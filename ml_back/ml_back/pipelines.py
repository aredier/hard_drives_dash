import pandas as pd
from chariots import nodes, Pipeline, MLMode

from .utils import IS_LOCAL
from .callbacks import TimerLogger
from .ops.data_ops.dataframe_manipulation_ops import PreprocessDF, FilterDates, ComputeTarget, \
    TrainTestSplit, ToPandas, CastDF, JoinCols, DropSplitCols
from .ops.data_ops.feature_engieneering import ComputeStd, ComputeMean, ComputeVariations
from .ops.data_ops.io_ops import LoadDask, SaveDask, ReadParquet, LoadJson, FromNumpy
from .ops.ml_ops import LightGBMClassifier, Metrics, UnderSampling, LabelEncoderOp

fake_now = pd.to_datetime('2019-01-05')


DATA_PATH = '/opt/data/hard-drive-data-and-stats/data_Q1_2019/drive_stats_2019_Q1/2019-01-0*.csv' if IS_LOCAL else\
    'gcs://chariots-data/hard-drive-data-and-stats/data_Q1_2019/drive_stats_2019_Q1/2019-01-0*.csv'
TRAIN_CKPT_PATH = '/opt/data/ckpt/train.parquet' if IS_LOCAL else 'gcs://chariots-data/ckpt/train.parquet'
TEST_CKPT_PATH = '/opt/data/ckpt/test.parquet' if IS_LOCAL else 'gcs://chariots-data/ckpt/test.parquet'

create_train_test_datasets = Pipeline([
    nodes.Node(LoadDask(path=DATA_PATH), output_nodes=['dask_df']),
    nodes.Node(PreprocessDF(), input_nodes=['dask_df'], output_nodes=['preprocessed_df']),
    nodes.Node(FilterDates(fake_now), input_nodes=['preprocessed_df'], output_nodes=['filtered_df']),
    nodes.Node(ComputeTarget(), input_nodes=['filtered_df'], output_nodes=['df_with_target']),
    nodes.Node(TrainTestSplit(max_date=fake_now), input_nodes=['df_with_target'], output_nodes=['train_df', 'test_df']),
    nodes.Node(SaveDask(TRAIN_CKPT_PATH), input_nodes=['train_df']),
    nodes.Node(SaveDask(TEST_CKPT_PATH), input_nodes=['test_df']),
], name='create_train_test_datasets', pipeline_callbacks=[TimerLogger()], use_worker=True)

_preprocessing_pipe = Pipeline([
    nodes.Node(CastDF(), input_nodes=['__pipeline_input__'], output_nodes=['typed_df']),
    nodes.Node(ComputeVariations(), input_nodes=['typed_df'], output_nodes=['df_with_variations']),
    nodes.Node(ComputeMean(), input_nodes=['df_with_variations'], output_nodes=['df_with_mean']),
    nodes.Node(ComputeStd(), input_nodes=['df_with_mean'], output_nodes=['__pipeline_output__'])
], name='preprocessing', pipeline_callbacks=[TimerLogger()])

train_pipe = Pipeline([
    nodes.Node(ReadParquet(TRAIN_CKPT_PATH), output_nodes=['dask_df']),
    nodes.Node(ToPandas(), input_nodes=['dask_df'], output_nodes=['pandas_df']),
    nodes.Node(_preprocessing_pipe, input_nodes=['pandas_df'], output_nodes=['preprocessed_df']),
    nodes.Node(UnderSampling(under_sampling_frac=.01), input_nodes=['preprocessed_df'], output_nodes=['sampled_df']),
    nodes.Node(DropSplitCols(), input_nodes=['sampled_df'], output_nodes=['numerical_dataset', 'models']),
    nodes.Node(LabelEncoderOp(mode=MLMode.FIT_PREDICT), input_nodes=['models'], output_nodes=['models_encoded']),
    nodes.Node(JoinCols(extract_target=True), input_nodes=['numerical_dataset', 'models_encoded'], output_nodes=['dataset_for_training', 'y_true']),
    # nodes.Node(LightGBMClassifier(mode=MLMode.FIT_PREDICT), input_nodes=['dataset_for_training'], output_nodes=['y_pred']),
    nodes.Node(Metrics(), input_nodes=['y_true', 'dataset_for_training'], output_nodes=['__pipeline_output__'])
], name='training', pipeline_callbacks=[TimerLogger()], use_worker=True)

test_pipe = Pipeline([
    nodes.Node(ReadParquet(TEST_CKPT_PATH), output_nodes=['dask_df']),
    nodes.Node(ToPandas(), input_nodes=['dask_df'], output_nodes=['pandas_df']),
    nodes.Node(_preprocessing_pipe, input_nodes=['pandas_df'], output_nodes=['preprocessed_df']),
    nodes.Node(DropSplitCols(), input_nodes=['preprocessed_df'], output_nodes=['numerical_dataset', 'models']),
    nodes.Node(LabelEncoderOp(mode=MLMode.PREDICT), input_nodes=['models'], output_nodes=['models_encoded']),
    nodes.Node(JoinCols(extract_target=True), input_nodes=['numerical_dataset', 'models_encoded'], output_nodes=['dataset_for_training', 'y_true']),
    nodes.Node(LightGBMClassifier(mode=MLMode.PREDICT), input_nodes=['dataset_for_training'], output_nodes=['y_pred']),
    nodes.Node(Metrics(), input_nodes=['y_true', 'y_pred'], output_nodes=['__pipeline_output__'])
], name='testing', pipeline_callbacks=[TimerLogger()], use_worker=True)


pred_pipe = Pipeline([
    nodes.Node(LoadJson(), input_nodes=['__pipeline_input__'], output_nodes=['pandas_df']),
    nodes.Node(PreprocessDF(), input_nodes=['pandas_df'], output_nodes=['pre_preprocessed_df']),
    nodes.Node(CastDF(is_pred=True), input_nodes=['pre_preprocessed_df'], output_nodes=['typed_df']),
    nodes.Node(ComputeVariations(), input_nodes=['typed_df'], output_nodes=['df_with_variations']),
    nodes.Node(ComputeMean(), input_nodes=['df_with_variations'], output_nodes=['df_with_mean']),
    nodes.Node(ComputeStd(), input_nodes=['df_with_mean'], output_nodes=['preprocessed_df']),
    nodes.Node(DropSplitCols(), input_nodes=['preprocessed_df'], output_nodes=['numerical_dataset', 'models']),
    nodes.Node(LabelEncoderOp(mode=MLMode.PREDICT), input_nodes=['models'], output_nodes=['models_encoded']),
    nodes.Node(JoinCols(extract_target=False), input_nodes=['numerical_dataset', 'models_encoded'], output_nodes=['dataset_for_training']),
    nodes.Node(LightGBMClassifier(mode=MLMode.PREDICT), input_nodes=['dataset_for_training'], output_nodes=['predictions']),
    nodes.Node(FromNumpy(), input_nodes=['predictions'], output_nodes=['__pipeline_output__']),
], name='prediction', pipeline_callbacks=[TimerLogger()])