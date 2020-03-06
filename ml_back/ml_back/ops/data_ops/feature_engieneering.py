import re

import pandas as pd
from chariots import base


class ComputeStd(base.BaseOp):

    def execute(self, pdf):
        data_cols = [col for col in pdf.columns if re.match('^smart_\d+_normalized$', col)]
        week_std = pdf.groupby('serial_number')[data_cols].rolling(
            window=7, min_periods=1
        ).std(ddof=0)
        week_std.columns = [col + '_7d_std' for col in week_std.columns]
        return pd.concat([pdf, week_std.droplevel('serial_number')], axis=1, sort=True)


class ComputeMean(base.BaseOp):

    def execute(self, pdf):
        data_cols = [col for col in pdf.columns if col.startswith('smart')]

        week_rolling = pdf.groupby('serial_number')[data_cols].rolling(
            window=7, min_periods=1
        ).mean()
        week_rolling.columns = [col + '_7d_rolling' for col in week_rolling.columns]
        return pd.concat([pdf, week_rolling.droplevel('serial_number')], axis=1, sort=True)


class ComputeVariations(base.BaseOp):

    def execute(self, pdf):
        data_cols = [col for col in pdf.columns if col.startswith('smart')]

        def compute_variations(x):
            values = np.concatenate([np.zeros((1, x.shape[1])), np.diff(x, axis=0) / np.abs(x[:-1])])
            return pd.DataFrame(values, index=x.index)

        variation = pdf.groupby('serial_number')[data_cols].apply(compute_variations)
        variation.columns = [col + '_variation' for col in data_cols]

        return pd.concat([pdf, variation], axis=1)