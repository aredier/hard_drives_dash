import re

from chariots import versioning, base
from dask import dataframe as dd
import pandas as pd
import numpy as np

from ...constants import COLS_TO_DROP


class PreprocessDF(base.BaseOp):
    
    def __init__(self, is_dask=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_dask = is_dask
        
    cols_to_drop = versioning.VersionedField(
      COLS_TO_DROP,
        versioning.VersionType.MAJOR
    )
    start_time = versioning.VersionedField(pd.Timestamp(year=2019, day=1, month=1), versioning.VersionType.MAJOR)

    def execute(self, dask_df):
        print(dask_df.shape)
        cols_name = []
        for col in dask_df.columns:
            match = re.match(r'^(smart_\d+)_', col)
            if match is not None and match.group(1) in self.cols_to_drop:
                cols_name.append(col)
        dask_df = dask_df.drop(cols_name, axis=1)
        raw_cols = [col for col in dask_df.columns if re.match(r'^smart_\d+_raw', col)]
        dask_df = dask_df.drop(raw_cols, axis=1)
        if self.is_dask:
            dask_df['date'] = dd.to_datetime(dask_df['date'])
        else:
            dask_df['date'] = pd.to_datetime(dask_df['date'])
        dask_df['index_hash'] = dask_df.apply(
            lambda x: x['serial_number'] + '__' + str((x['date'] - self.start_time).days), axis=1)
        
        print(dask_df.shape)
        return dask_df.set_index('index_hash')


class ComputeTarget(base.BaseOp):
    start_time = versioning.VersionedField(pd.Timestamp(year=2019, day=1, month=1), versioning.VersionType.MAJOR)

    def execute(self, dask_df):
        target = dask_df.loc[:, ['failure', 'date', 'serial_number']]
        target['index_hash'] = target.apply(
            lambda x: x['serial_number'] + '__' + str((x['date'] - self.start_time).days - 1), axis=1)
        target = target.compute()
        df_with_target = dask_df.join(target.set_index('index_hash').drop(['serial_number', 'date'], axis=1),
                                      how='inner', rsuffix='_1d')
        return df_with_target


class TrainTestSplit(base.BaseOp):
    
    
    def __init__(self, max_date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_date = pd.datetime(year=2019, month=1, day=1)
        
        self.separation_date = max_date - pd.Timedelta(days=int(abs((start_date - max_date).days) // 3))
    
    
    def execute(self, dask_df):
        train_idx = dask_df.date < self.separation_date
        return dask_df[train_idx], dask_df[~train_idx]


class FilterDates(base.BaseOp):
    def __init__(self, date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date

    def execute(self, dask_df):
        print(dask_df.shape)
        return dask_df[dask_df.date <= self.date]


class ToPandas(base.BaseOp):

    def execute(self, dask_df):
        # bug with pipeline usage
        if isinstance(dask_df, list):
            dask_df = dask_df[0]
        res = dask_df.compute()
        return res.reindex(sorted(res.columns), axis=1)

class CastDF(base.BaseOp):
    
    def __init__(self, is_pred=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_pred = is_pred

    def execute(self, pdf):

        # forgot to drop a col
        if isinstance(pdf, list):
            pdf = pdf[0]
        print(pdf.shape)
            
        pdf = pdf.drop('smart_255_normalized', axis=1)
        if self.is_pred:
            print(pdf.shape)
            pdf.fillna(0.0)
            print(pdf.head(3))
        else:
            pdf = pdf.dropna()
        print(pdf.shape)
        for feature in pdf.columns:
            if not feature.startswith('smart'):
                continue
            pdf[feature] = pdf[feature].astype(np.float32)
        return pdf


class DropSplitCols(base.BaseOp):

    def execute(self, pdf):
        print(pdf.shape)
        return pdf.drop(['date', 'serial_number', 'model', 'failure', ], axis=1).fillna(0), pdf.model


class JoinCols(base.BaseOp):

    def __init__(self, extract_target=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extract_target = extract_target

    def execute(self, numerical_dataset, models_encoded):
        
        print(numerical_dataset.shape)
        numerical_dataset['model_labeled'] = models_encoded
        if self.extract_target:
            return numerical_dataset, numerical_dataset.failure_1d

        return numerical_dataset