import time

import structlog
from chariots import callbacks


log = structlog.getLogger('callbacks')


class TimerLogger(callbacks.PipelineCallback):

    def __init__(self):
        self.start_times = {}

    def before_node_execution(self, pipeline, node, args):
        self.start_times[node.name] = time.time()

    def after_node_execution(self, pipeline, node, args, output):
        exec_time = time.time() - self.start_times[node.name]
        log.info('[DONE] node: {} in {}'.format(node.name, exec_time))