import os
import datetime as dt
from multiprocessing.pool import ThreadPool

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from chariots import Client

from ml_back import pipelines
from common_utils import db, date_utils


IS_LOCAL = os.environ.get('CHARIOTS_LOCAL') == 'true'
client = Client(backend_url='http://web-flask-internal:5000')

db_user_name = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST', '127.0.0.1')

if IS_LOCAL:
    engine = create_engine('postgresql://aredier2@docker.for.mac.localhost:5432/mydb')
else:
    engine = create_engine('postgresql+pg8000://{}@{}/{}'.format(db_user_name, db_host, db_name))

Session = sessionmaker(engine)
session = Session()

LOOK_BACK_MIN = os.environ.get('LOOK_BACK_MIN', 2)

if IS_LOCAL:
    fake_now = date_utils.get_fake_today()
else:
    fake_now = dt.datetime.utcnow() - dt.timedelta(days=200)
look_back = fake_now - dt.timedelta(minutes=LOOK_BACK_MIN)

query = session.\
    query(db.HardDriveStatus.serial_number).\
    filter(db.HardDriveStatus.date <= fake_now).\
    filter(db.HardDriveStatus.date > look_back)
selected_serial_number = [x[0] for x in query]

all_for_data_query = session\
    .query(db.HardDriveStatus)\
    .filter(db.HardDriveStatus.serial_number.in_(selected_serial_number))\
    .filter(db.HardDriveStatus.date > look_back - dt.timedelta(days=8))

pandas_result = pd.read_sql(all_for_data_query.statement, all_for_data_query.session.bind)
pandas_result = pandas_result.set_index('id')
pandas_result = pandas_result.drop('prediction', axis=1)
pandas_result['date'] = pandas_result.date.astype(str)

response = client.call_pipeline(pipelines.pred_pipe, pipeline_input=pandas_result.to_dict(orient='record'))

pandas_result['date'] = pd.to_datetime(pandas_result.date)


def update_prediction(update_input):
    local_session = Session()
    (row_id, row), prediction = update_input
    if row['date'] < look_back + dt.timedelta(minutes=1):
        return
    el = local_session.query(db.HardDriveStatus).filter(db.HardDriveStatus.id == row_id).first()
    el.prediction = prediction
    local_session.commit()


with ThreadPool(10) as pool:
    max_records = len(response.value)
    for i, _ in enumerate(pool.map(update_prediction, zip(pandas_result.iterrows(), response.value))):
        if not i % 1000:
            print('{} done out of {}, {}%'.format(i, max_records, i/max_records))
