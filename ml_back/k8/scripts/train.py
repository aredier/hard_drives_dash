import os
import time
import datetime as dt

import structlog
from chariots import Client, workers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ml_back import pipelines
from common_utils import db


IS_LOCAL = os.environ.get('CHARIOTS_LOCAL') == 'true'
db_user_name = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS', 'none')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST', '127.0.0.1')

if IS_LOCAL:
    engine = create_engine('postgresql+pg8000://aredier2@docker.for.mac.localhost:5432/mydb')
else:
    engine = create_engine('postgresql+pg8000://{}@{}/{}'.format(db_user_name, db_host, db_name))


log = structlog.getLogger('callbacks')
client = Client(backend_url='http://web-flask-internal:5000')
Session = sessionmaker(bind=engine)


def await_pipeline_execution(response, pipeline):
    update = client.fetch_job(response.job_id, pipeline)
    while update.job_status in [workers.JobStatus.running, workers.JobStatus.queued]:
        log.info(str(update.job_status))
        time.sleep(30)
        update = client.fetch_job(response.job_id, pipeline)
    log.info(str(update.job_status))
    return update


log.info('splitting the data')
response = client.call_pipeline(pipelines.create_train_test_datasets)
final_response = await_pipeline_execution(response, pipelines.create_train_test_datasets)

if final_response.job_status == workers.JobStatus.failed:
    raise ValueError('pipeline failed')

# sleeping to let workers recover
time.sleep(60)


log.info('training the model')
response = client.call_pipeline(pipelines.train_pipe)
final_response = await_pipeline_execution(response, pipelines.train_pipe)

if final_response.job_status == workers.JobStatus.failed:
    raise ValueError('pipeline failed')

performances = db.ModelPerformance(
    date=dt.datetime.utcnow(),
    recall={
        0.5: final_response.value['recall_05'],
        0.05: final_response.value['recall_005']
    },
    precision={
        0.5: final_response.value['precision_05'],
        0.05: final_response.value['precision_005']
    },
    roc_auc=final_response.value['roc_auc'],
    f1_score={
        0.5: final_response.value['recall_05'],
        0.05: final_response.value['f1_score_005']
    },
    confusion_matrix={
        0.5: final_response.value['confusion_05'],
        0.05: final_response.value['confusion_005']
    },
    is_live_perf=False,
    is_training_performance=True,
)

session = Session()
session.add(performances)
session.commit()

# sleeping to let workers recover
time.sleep(60)
log.info('testing the model')

response = client.call_pipeline(pipelines.test_pipe)
final_response = await_pipeline_execution(response, pipelines.test_pipe)

if final_response.job_status == workers.JobStatus.failed:
    raise ValueError('pipeline failed')

performances = db.ModelPerformance(
    date=dt.datetime.utcnow(),
    recall={
        0.5: final_response.value['recall_05'],
        0.05: final_response.value['recall_005']
    },
    precision={
        0.5: final_response.value['precision_05'],
        0.05: final_response.value['precision_005']
    },
    roc_auc=final_response.value['roc_auc'],
    f1_score={
        0.5: final_response.value['recall_05'],
        0.05: final_response.value['f1_score_005']
    },
    confusion_matrix={
        0.5: final_response.value['confusion_05'],
        0.05: final_response.value['confusion_005']
    },
    is_live_perf=False,
    is_training_performance=False,
)
session = Session()
session.add(performances)
session.commit()
