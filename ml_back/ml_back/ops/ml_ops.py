import io
import os
import tempfile
from typing import Any

import pandas as pd
from chariots import base, sklearn, versioning
from chariots.base import BaseSerializer
from sklearn import metrics

from .utils import LabelEncoderExt


class UnderSampling(base.BaseOp):

    def __init__(self, under_sampling_frac, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.under_sampling_frac = under_sampling_frac

    def execute(self, pdf):
        positives_idx = pdf.failure_1d == 1
        return pd.concat(
            [
                pdf[positives_idx],
                pdf[~positives_idx].sample(frac=self.under_sampling_frac)
            ],
            axis=0
        ).sample(frac=1)


class LabelEncoderOp(sklearn.SKUnsupervisedOp):
    model_class = versioning.VersionedField(LabelEncoderExt, versioning.VersionType.MAJOR)
    training_update_version = versioning.VersionType.MAJOR

class LightGBMerializer(BaseSerializer):
    """
    serializes objects using the dill library (similar to pickle but optimized for numpy arrays.
    """

    def serialize_object(self, target: Any) -> bytes:
        with tempfile.tempdir() as dir:
            file_path = os.path.join(dir, 'model.txt')
            target.save_model(file_path)
            with open(file_path, 'rb') as bytes_file:
                return bytes_file.read()

    def deserialize_object(self, serialized_object: bytes) -> Any:
        import lightgbm
        with tempfile.TemporaryDirectory() as dir:
            file_path = os.path.join(dir, 'model.txt')
            with open(file_path, 'wb') as bytes_file:
                return bytes_file.write(serialized_object)
            return lightgbm.Booster(model_file='model.txt')


class LightGBMClassifier(base.BaseMLOp):
    model_parameters = versioning.VersionedFieldDict(
        versioning.VersionType.MINOR,
        {
            'is_unbalance': True,
            'boosting_type': 'gbdt',
            'learning_rate': 0.001,
            'max_depth': -1,
            'n_estimators': 3000,
            'num_leaves': 25,
            'subsample': 0.6,  # Subsample ratio of the training instance.
            'subsample_freq': 0,  # frequence of subsample, <=0 means no enable
            'colsample_bytree': 0.3,  # Subsample ratio of columns when constructing each tree.
            'max_bin': 255,  # Number of bucketed bin for feature values'
        })

    dataset_parameters = versioning.VersionedFieldDict(
        versioning.VersionType.MINOR,
        {
            'categorical_feature': ['model_labeled']
        })

    target_col = versioning.VersionedField('failure_1d', versioning.VersionType.MAJOR)
    serializer_cls = LightGBMerializer

    def _init_model(self):
        return None

    def fit(self, train_data):
        import lightgbm
        train_dataset = lightgbm.Dataset(
            data=train_data.drop([self.target_col], axis=1),
            label=train_data[self.target_col],
            **self.dataset_parameters
        )

        self._model = lightgbm.train(
            self.model_parameters,
            train_dataset,
        )
        print("+++++++++++++++ DONE TRAINING ++++++++++++++++++")

    def predict(self, prediction_data):
        pass
        if self.target_col in prediction_data.columns:
            prediction_data = prediction_data.drop([self.target_col], axis=1)
        return self._model.predict(prediction_data)

    def __getstate__(self):
        self._model = None
        return self.__dict__


class Metrics(base.BaseOp):

    def execute(self, y_true, y_pred):
        return {
            'roc_auc': metrics.roc_auc_score(y_true, y_pred),

            # threshold
            'f1_score_05': metrics.f1_score(y_true, y_pred > 0.5),
            'recall_05': metrics.recall_score(y_true, y_pred > 0.5),
            'precision_05': metrics.precision_score(y_true, y_pred > 0.5),
            'confusion_05': metrics.confusion_matrix(y_true, y_pred > 0.5).tolist(),
            # other threshold
            'f1_score_005': metrics.f1_score(y_true, y_pred > 0.05),
            'recall_005': metrics.recall_score(y_true, y_pred > 0.05),
            'precision_005': metrics.precision_score(y_true, y_pred > 0.05),
            'confusion_005': metrics.confusion_matrix(y_true, y_pred > 0.05).tolist(),
        }