from google.cloud import storage
from chariots import runners, savers, workers, OpStore, Chariots

from redis import Redis


from .pipelines import create_train_test_datasets, train_pipe, test_pipe

storage_client = storage.Client()
bucket = storage_client.bucket('op_store')
op_store = OpStore(saver=savers.GoogleStorageSaver(root_path='op_store', bucket=bucket))
runner = runners.SequentialRunner()
worker_pool = workers.RQWorkerPool(Redis())

app = Chariots(
    app_pipelines=[
        create_train_test_datasets,
        train_pipe,
        test_pipe
    ], runner=runner, op_store=op_store, worker_pool=worker_pool, import_name='app')

