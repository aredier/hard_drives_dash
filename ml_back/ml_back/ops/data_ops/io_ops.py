import os
import json

from chariots import base
import dask.dataframe as dd
import pandas as pd


class LoadDask(base.BaseOp):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    def execute(self):
        return dd.read_csv(self.path)


class SaveDask(base.BaseOp):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path

    def execute(self, dask_df):
        dask_df = dask_df.fillna(value=dask_df.mean(axis=1))
        dask_df.to_parquet(self.path)


class ReadParquet(base.BaseOp):

    def __init__(self, path, index='index_hash', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.index = index

    def execute(self):
        return dd.read_parquet(self.path, index=self.index)
    

class LoadJson(base.BaseOp):
    def __init__(self, index='index_hash', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index
    
    def execute(self, json_data):
        res = pd.DataFrame(json_data)
#         res = res.set_index(self.index)
        print(res.shape)
        return res.reindex(sorted(res.columns), axis=1)
    

class FromNumpy(base.BaseOp):
    
    def execute(self, np_data):
        return np_data.tolist()
