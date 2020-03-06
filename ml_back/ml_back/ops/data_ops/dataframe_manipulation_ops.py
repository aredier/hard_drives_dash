import re

from chariots import versioning, base
from dask import dataframe as dd
import pandas as pd

from ...constants import COLS_TO_DROP


class PreprocessDF(base.BaseOp):
    cols_to_drop = versioning.VersionedField(
      COLS_TO_DROP,
        versioning.VersionType.MAJOR
    )
    start_time = versioning.VersionedField(pd.Timestamp(year=2019, day=1, month=1), versioning.VersionType.MAJOR)

    def execute(self, dask_df):
        cols_name = []
        for col in dask_df.columns:
            match = re.match(r'^(smart_\d+)_', col)
            if match is not None and match.group(1) in self.cols_to_drop:
                cols_name.append(col)
        dask_df = dask_df.drop(cols_name, axis=1)
        raw_cols = [col for col in dask_df.columns if re.match(r'^smart_\d+_raw', col)]
        dask_df = dask_df.drop(raw_cols, axis=1)
        dask_df['date'] = dd.to_datetime(dask_df['date'])
        dask_df['index_hash'] = dask_df.apply(
            lambda x: x['serial_number'] + '__' + str((x['date'] - self.start_time).days), axis=1)
        return dask_df


class ComputeTarget(base.BaseOp):
    start_time = versioning.VersionedField(pd.Timestamp(year=2019, day=1, month=1), versioning.VersionType.MAJOR)

    def execute(self, dask_df):
        target = dask_df.loc[:, ['failure', 'date', 'serial_number']]
        target['index_hash'] = target.apply(
            lambda x: x['serial_number'] + '__' + str((x['date'] - self.start_time).days - 1), axis=1)
        target = target.compute()
        df_with_target = dask_df.join(target.set_index('index_hash').drop(['serial_number', 'date'], axis=1),
                                      on='index_hash', how='inner', rsuffix='_1d')
        return df_with_target


class TrainTestSplit(base.BaseOp):
    separation_date = versioning.VersionedField(pd.Timestamp(year=2019, day=5, month=1), versioning.VersionType.MINOR)

    def execute(self, dask_df):
        train_idx = dask_df.date < self.separation_date
        return dask_df[train_idx], dask_df[~train_idx]


class FilterDates(base.BaseOp):
    def __init__(self, date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date

    def execute(self, dask_df):
        return dask_df[dask_df.date < self.date]


class ToPandas(base.BaseOp):

    def execute(self, dask_df):
        # bug with pipeline usage
        if isinstance(dask_df, list):
            dask_df = dask_df[0]
        return dask_df.compute()


class CastDF(base.BaseOp):

    def execute(self, pdf):

        # forgot to drop a col

        pdf = pdf.drop('smart_255_normalized', axis=1)
        pdf = pdf.dropna()
        for feature in pdf.columns:
            if not feature.startswith('smart'):
                continue
            pdf[feature] = pdf[feature].astype(np.float32)
        return pdf


class DropSplitCols(base.BaseOp):

    def execute(self, pdf):
        return pdf.drop(['date', 'serial_number', 'model', 'failure', ], axis=1).fillna(0), pdf.model


class JoinCols(base.BaseOp):

    def __init__(self, extract_target=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extract_target = extract_target

    def execute(self, numerical_dataset, models_encoded):
        numerical_dataset['model_labeled'] = models_encoded
        if self.extract_target:
            return numerical_dataset, numerical_dataset.failure_1d

        return numerical_dataset