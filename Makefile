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

