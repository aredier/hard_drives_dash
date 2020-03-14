from google.cloud import storage
from chariots import runners, savers, workers, OpStore, Chariots

from redis import Redis


from .pipelines import create_train_test_datasets, train_pipe, test_pipe, pred_pipe

storage_client = storage.Client()
bucket = storage_client.bucket('op_store')
runner = runners.SequentialRunner()
worker_pool = workers.RQWorkerPool(Redis(), queue_kwargs={'default_timeout': 10000})

app = Chariots(
    app_pipelines=[
        create_train_test_datasets,
        train_pipe,
        test_pipe,
        pred_pipe
    ], 
    runner=runner,
    saver_cls=savers.GoogleStorageSaver,
    saver_kwargs={
       'bucket_name': 'op_store', 
    }, 
    path='prod_test/', 
    worker_pool=worker_pool, 
    import_name='app')


if __name__ == '__main__':
    app._worker_pool.spawn_worker()
    app.run()

