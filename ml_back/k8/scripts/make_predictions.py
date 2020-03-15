import os
import datetime as dt
import requests
from multiprocessing.pool import ThreadPool

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from chariots import Client

from ml_back import pipelines
from common_utils import db


client = Client(backend_url='http://10.128.0.10:80')
db_password = requests.get("http://metadata/computeMetadata/v1/project/attributes/db_password",
         headers={'Metadata-Flavor': 'Google'}).text
db_user_name = requests.get("http://metadata/computeMetadata/v1/project/attributes/db_user_name",
         headers={'Metadata-Flavor': 'Google'}).text

engine = create_engine('postgresql://{}:{}@35.239.139.214'.format(db_user_name, db_password))
Session = sessionmaker(engine)
session = Session()

LOOK_BACK_MIN = os.environ.get('LOOK_BACK_MIN', 5)

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


def update_prediction(update_input):
    local_session = Session()
    (row_id, _), prediction = update_input
    el = local_session.query(db.HardDriveStatus).filter(db.HardDriveStatus.id == row_id).first()
    el.prediction = prediction
    local_session.commit()


with ThreadPool(10) as pool:
    _ = pool.map(update_prediction, zip(pandas_result.iterrows(), response.value))