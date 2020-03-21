from google.cloud import storage
from chariots import runners, savers, workers, OpStore, Chariots

from redis import Redis
from .utils import IS_LOCAL


from .pipelines import create_train_test_datasets, train_pipe, test_pipe, pred_pipe

if not IS_LOCAL:
    storage_client = storage.Client()
    saver_cls = savers.GoogleStorageSaver
    saver_kwargs = {
        'bucket_name': 'op_store',
    }
else:
    saver_cls = savers.FileSaver
    saver_kwargs = {'root_path': '/opt/data/op_store'}

runner = runners.SequentialRunner()
worker_pool = workers.RQWorkerPool(Redis('redis-master', port=6379), queue_kwargs={'default_timeout': 10000})

app = Chariots(
    app_pipelines=[
        create_train_test_datasets,
        train_pipe,
        test_pipe,
        pred_pipe
    ], 
    runner=runner,
    saver_cls=saver_cls,
    saver_kwargs=saver_kwargs,
    path='/opt/data/op_store' if IS_LOCAL else '/op_store',
    worker_pool=worker_pool, 
    import_name='app')
