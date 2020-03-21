docker:
	docker system prune --force
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/common:latest -f common_utils/Dockerfile.common common_utils/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/common-chariots:latest -f ml_back/Dockerfile ml_back/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/cahriots-server:latest -f ml_back/k8/chariots_server/Dockerfile.server ml_back/k8/chariots_server/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/cahriots-workers:latest -f ml_back/k8/chariots_worker/Dockerfile.worker ml_back/k8/chariots_worker/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/redis-db:latest -f ml_back/k8/redis/Dockerfile.redis ml_back/k8/redis/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/chariots-scripts:latest -f ml_back/k8/scripts/Dockerfile ml_back/k8/scripts/

docker-push:
	docker push eu.gcr.io/chariots-poc/ml_back/common:latest
	docker push eu.gcr.io/chariots-poc/ml_back/common-chariots:latest
	docker push eu.gcr.io/chariots-poc/ml_back/cahriots-server:latest
	docker push eu.gcr.io/chariots-poc/ml_back/cahriots-workers:latest
	docker push eu.gcr.io/chariots-poc/ml_back/redis-db:latest
	docker push eu.gcr.io/chariots-poc/ml_back/chariots-scripts:latest


local-tear-down:
	kubectl delete svc local-proxy
	kubectl delete svc redis-master
	kubectl delete svc web-flask-internal
	kubectl delete deployment web-flask
	kubectl delete deployment rq-worker
	kubectl delete deployment redis-master

local-deploy:
	kubectl apply -f ml_back/k8/redis/redis-local.yaml
	kubectl apply -f ml_back/k8/chariots_server/chariots_server_local.yaml
	kubectl apply -f ml_back/k8/chariots_worker/chariots-worker-local.yaml


remote-deploy:
	kubectl apply -f ml_back/k8/redis/redis.yaml
	kubectl apply -f ml_back/k8/chariots_server/chariots_server.yaml
	kubectl apply -f ml_back/k8/chariots_worker/chariots-worker.yaml
	#kubectl apply -f ml_back/k8/scripts/predictions.yaml

remote-tear-down:
	kubectl delete svc redis-master
	kubectl delete svc web-flask-internal
	kubectl delete deployment rq-worker
	kubectl delete deployment redis-master
	kubectl delete deployment web-flask
	#kubectl delete CronJob predictions

b'\x80\x03cchariots._pipeline\nPipeline\nq\x00)\x81q\x01}q\x02(X\t\x00\x00\x00callbacksq\x03]q\x04cml_back.callbacks\nTimerLogger\nq\x05)\x81q\x06}q\x07X\x0b\x00\x00\x00start_timesq\x08}q\tsbaX\x06\x00\x00\x00_graphq\n]q\x0b(cchariots.nodes._node\nNode\nq\x0c)\x81q\r}q\x0e(X\x03\x00\x00\x00_opq\x0fcml_back.ops.data_ops.io_ops\nReadParquet\nq\x10)\x81q\x11}q\x12(h\x03]q\x13X\x04\x00\x00\x00pathq\x14X&\x00\x00\x00gcs://chariots-data/ckpt/train.parquetq\x15X\x05\x00\x00\x00indexq\x16X\n\x00\x00\x00index_hashq\x17ubX\x0b\x00\x00\x00input_nodesq\x18]q\x19X\x0c\x00\x00\x00output_nodesq\x1a]q\x1bX\x07\x00\x00\x00dask_dfq\x1caubh\x0c)\x81q\x1d}q\x1e(h\x0fcml_back.ops.data_ops.dataframe_manipulation_ops\nToPandas\nq\x1f)\x81q }q!h\x03]q"sbh\x18]q#cchariots.base._base_nodes\nNodeReference\nq$)\x81q%}q&(X\x04\x00\x00\x00nodeq\'h\rX\t\x00\x00\x00referenceq(h\x1cubah\x1a]q)X\t\x00\x00\x00pandas_dfq*aubh\x0c)\x81q+}q,(h\x0fh\x00)\x81q-}q.(h\x03]q/h\x05)\x81q0}q1h\x08}q2sbah\n]q3(h\x0c)\x81q4}q5(h\x0fcml_back.ops.data_ops.dataframe_manipulation_ops\nCastDF\nq6)\x81q7}q8(h\x03]q9X\x07\x00\x00\x00is_predq:\x89ubh\x18]q;h$)\x81q<}q=(h\'cchariots.base._base_nodes\nReservedNodes\nq>X\x12\x00\x00\x00__pipeline_input__q?\x85q@RqAh(h?ubah\x1a]qBX\x08\x00\x00\x00typed_dfqCaubh\x0c)\x81qD}qE(h\x0fcml_back.ops.data_ops.feature_engieneering\nComputeVariations\nqF)\x81qG}qHh\x03]qIsbh\x18]qJh$)\x81qK}qL(h\'h4h(hCubah\x1a]qMX\x12\x00\x00\x00df_with_variationsqNaubh\x0c)\x81qO}qP(h\x0fcml_back.ops.data_ops.feature_engieneering\nComputeMean\nqQ)\x81qR}qSh\x03]qTsbh\x18]qUh$)\x81qV}qW(h\'hDh(hNubah\x1a]qXX\x0c\x00\x00\x00df_with_meanqYaubh\x0c)\x81qZ}q[(h\x0fcml_back.ops.data_ops.feature_engieneering\nComputeStd\nq\\)\x81q]}q^h\x03]q_sbh\x18]q`h$)\x81qa}qb(h\'hOh(hYubah\x1a]qcX\x13\x00\x00\x00__pipeline_output__qdaubeX\x05\x00\x00\x00_nameqeX\r\x00\x00\x00preprocessingqfX\n\x00\x00\x00use_workerqgNubh\x18]qhh$)\x81qi}qj(h\'h\x1dh(h*ubah\x1a]qkX\x0f\x00\x00\x00preprocessed_dfqlaubh\x0c)\x81qm}qn(h\x0fcml_back.ops.ml_ops\nUnderSampling\nqo)\x81qp}qq(h\x03]qrX\x13\x00\x00\x00under_sampling_fracqsG?\x84z\xe1G\xae\x14{ubh\x18]qth$)\x81qu}qv(h\'h+h(hlubah\x1a]qwX\n\x00\x00\x00sampled_dfqxaubh\x0c)\x81qy}qz(h\x0fcml_back.ops.data_ops.dataframe_manipulation_ops\nDropSplitCols\nq{)\x81q|}q}h\x03]q~sbh\x18]q\x7fh$)\x81q\x80}q\x81(h\'hmh(hxubah\x1a]q\x82(X\x11\x00\x00\x00numerical_datasetq\x83X\x06\x00\x00\x00modelsq\x84eubh\x0c)\x81q\x85}q\x86(h\x0fcml_back.ops.ml_ops\nLabelEncoderOp\nq\x87)\x81q\x88}q\x89(h\x03]q\x8aX\n\x00\x00\x00_call_modeq\x8bcchariots._ml_mode\nMLMode\nq\x8cX\x0b\x00\x00\x00fit_predictq\x8d\x85q\x8eRq\x8fX\n\x00\x00\x00serializerq\x90cchariots.serializers._dill_serializer\nDillSerializer\nq\x91)\x81q\x92X\x06\x00\x00\x00_modelq\x93cml_back.ops.utils\nLabelEncoderExt\nq\x94)\x81q\x95}q\x96X\r\x00\x00\x00label_encoderq\x97csklearn.preprocessing._label\nLabelEncoder\nq\x98)\x81q\x99}q\x9aX\x10\x00\x00\x00_sklearn_versionq\x9bX\x06\x00\x00\x000.22.1q\x9csbsbX\x13\x00\x00\x00_last_training_timeq\x9dK\x00ubh\x18]q\x9eh$)\x81q\x9f}q\xa0(h\'hyh(h\x84ubah\x1a]q\xa1X\x0e\x00\x00\x00models_encodedq\xa2aubh\x0c)\x81q\xa3}q\xa4(h\x0fcml_back.ops.data_ops.dataframe_manipulation_ops\nJoinCols\nq\xa5)\x81q\xa6}q\xa7(h\x03]q\xa8X\x0e\x00\x00\x00extract_targetq\xa9\x88ubh\x18]q\xaa(h$)\x81q\xab}q\xac(h\'hyh(h\x83ubh$)\x81q\xad}q\xae(h\'h\x85h(h\xa2ubeh\x1a]q\xaf(X\x14\x00\x00\x00dataset_for_trainingq\xb0X\x06\x00\x00\x00y_trueq\xb1eubh\x0c)\x81q\xb2}q\xb3(h\x0fcml_back.ops.ml_ops\nLightGBMClassifier\nq\xb4)\x81q\xb5}q\xb6(h\x03]q\xb7h\x8bh\x8fh\x90h\x91)\x81q\xb8h\x93Nh\x9dK\x00ubh\x18]q\xb9h$)\x81q\xba}q\xbb(h\'h\xa3h(h\xb0ubah\x1a]q\xbcX\x06\x00\x00\x00y_predq\xbdaubh\x0c)\x81q\xbe}q\xbf(h\x0fcml_back.ops.ml_ops\nMetrics\nq\xc0)\x81q\xc1}q\xc2h\x03]q\xc3sbh\x18]q\xc4(h$)\x81q\xc5}q\xc6(h\'h\xa3h(h\xb1ubh$)\x81q\xc7}q\xc8(h\'h\xb2h(h\xbdubeh\x1a]q\xc9hdaubeheX\x08\x00\x00\x00trainingq\xcahg\x88ub.'
b'\x80\x04\x95)\x08\x00\x00\x00\x00\x00\x00\x8c\x12chariots._pipeline\x94\x8c\x08Pipeline\x94\x93\x94)\x81\x94}\x94(\x8c\tcallbacks\x94]\x94\x8c\x11ml_back.callbacks\x94\x8c\x0bTimerLogger\x94\x93\x94)\x81\x94}\x94\x8c\x0bstart_times\x94}\x94sba\x8c\x06_graph\x94]\x94(\x8c\x14chariots.nodes._node\x94\x8c\x04Node\x94\x93\x94)\x81\x94}\x94(\x8c\x03_op\x94\x8c\x1bml_back.ops.data_ops.io_ops\x94\x8c\x0bReadParquet\x94\x93\x94)\x81\x94}\x94(h\x05]\x94\x8c\x04path\x94\x8c&gcs://chariots-data/ckpt/train.parquet\x94\x8c\x05index\x94\x8c\nindex_hash\x94ub\x8c\x0binput_nodes\x94]\x94\x8c\x0coutput_nodes\x94]\x94\x8c\x07dask_df\x94aubh\x12)\x81\x94}\x94(h\x15\x8c/ml_back.ops.data_ops.dataframe_manipulation_ops\x94\x8c\x08ToPandas\x94\x93\x94)\x81\x94}\x94h\x05]\x94sbh ]\x94\x8c\x19chariots.base._base_nodes\x94\x8c\rNodeReference\x94\x93\x94)\x81\x94}\x94(\x8c\x04node\x94h\x13\x8c\treference\x94h$ubah"]\x94\x8c\tpandas_df\x94aubh\x12)\x81\x94}\x94(h\x15h\x02)\x81\x94}\x94(h\x05]\x94h\t)\x81\x94}\x94h\x0c}\x94sbah\x0e]\x94(h\x12)\x81\x94}\x94(h\x15h\'\x8c\x06CastDF\x94\x93\x94)\x81\x94}\x94(h\x05]\x94\x8c\x07is_pred\x94\x89ubh ]\x94h0)\x81\x94}\x94(h3h.\x8c\rReservedNodes\x94\x93\x94\x8c\x12__pipeline_input__\x94\x85\x94R\x94h4hMubah"]\x94\x8c\x08typed_df\x94aubh\x12)\x81\x94}\x94(h\x15\x8c)ml_back.ops.data_ops.feature_engieneering\x94\x8c\x11ComputeVariations\x94\x93\x94)\x81\x94}\x94h\x05]\x94sbh ]\x94h0)\x81\x94}\x94(h3h@h4hQubah"]\x94\x8c\x12df_with_variations\x94aubh\x12)\x81\x94}\x94(h\x15hT\x8c\x0bComputeMean\x94\x93\x94)\x81\x94}\x94h\x05]\x94sbh ]\x94h0)\x81\x94}\x94(h3hRh4h^ubah"]\x94\x8c\x0cdf_with_mean\x94aubh\x12)\x81\x94}\x94(h\x15hT\x8c\nComputeStd\x94\x93\x94)\x81\x94}\x94h\x05]\x94sbh ]\x94h0)\x81\x94}\x94(h3h_h4hjubah"]\x94\x8c\x13__pipeline_output__\x94aube\x8c\x05_name\x94\x8c\rpreprocessing\x94\x8c\nuse_worker\x94Nubh ]\x94h0)\x81\x94}\x94(h3h%h4h6ubah"]\x94\x8c\x0fpreprocessed_df\x94aubh\x12)\x81\x94}\x94(h\x15\x8c\x12ml_back.ops.ml_ops\x94\x8c\rUnderSampling\x94\x93\x94)\x81\x94}\x94(h\x05]\x94\x8c\x13under_sampling_frac\x94G?\x84z\xe1G\xae\x14{ubh ]\x94h0)\x81\x94}\x94(h3h7h4h~ubah"]\x94\x8c\nsampled_df\x94aubh\x12)\x81\x94}\x94(h\x15h\'\x8c\rDropSplitCols\x94\x93\x94)\x81\x94}\x94h\x05]\x94sbh ]\x94h0)\x81\x94}\x94(h3h\x7fh4h\x8cubah"]\x94(\x8c\x11numerical_dataset\x94\x8c\x06models\x94eubh\x12)\x81\x94}\x94(h\x15h\x81\x8c\x0eLabelEncoderOp\x94\x93\x94)\x81\x94}\x94(h\x05]\x94\x8c\n_call_mode\x94\x8c\x11chariots._ml_mode\x94\x8c\x06MLMode\x94\x93\x94\x8c\x0bfit_predict\x94\x85\x94R\x94\x8c\nserializer\x94\x8c%chariots.serializers._dill_serializer\x94\x8c\x0eDillSerializer\x94\x93\x94)\x81\x94\x8c\x06_model\x94\x8c\x11ml_back.ops.utils\x94\x8c\x0fLabelEncoderExt\x94\x93\x94)\x81\x94}\x94\x8c\rlabel_encoder\x94\x8c\x1csklearn.preprocessing._label\x94\x8c\x0cLabelEncoder\x94\x93\x94)\x81\x94}\x94\x8c\x10_sklearn_version\x94\x8c\x060.22.1\x94sbsb\x8c\x13_last_training_time\x94K\x00ubh ]\x94h0)\x81\x94}\x94(h3h\x8dh4h\x99ubah"]\x94\x8c\x0emodels_encoded\x94aubh\x12)\x81\x94}\x94(h\x15h\'\x8c\x08JoinCols\x94\x93\x94)\x81\x94}\x94(h\x05]\x94\x8c\x0eextract_target\x94\x88ubh ]\x94(h0)\x81\x94}\x94(h3h\x8dh4h\x98ubh0)\x81\x94}\x94(h3h\x9ah4h\xc0ubeh"]\x94(\x8c\x14dataset_for_training\x94\x8c\x06y_true\x94eubh\x12)\x81\x94}\x94(h\x15h\x81\x8c\x12LightGBMClassifier\x94\x93\x94)\x81\x94}\x94(h\x05]\x94h\xa1h\xa7h\xa8h\xab)\x81\x94h\xadNh\xbbK\x00ubh ]\x94h0)\x81\x94}\x94(h3h\xc1h4h\xcfubah"]\x94\x8c\x06y_pred\x94aubh\x12)\x81\x94}\x94(h\x15h\x81\x8c\x07Metrics\x94\x93\x94)\x81\x94}\x94h\x05]\x94sbh ]\x94(h0)\x81\x94}\x94(h3h\xc1h4h\xd0ubh0)\x81\x94}\x94(h3h\xd1h4h\xddubeh"]\x94hvaubehw\x8c\x08training\x94hy\x88ub.'