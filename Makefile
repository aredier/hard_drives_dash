docker:
	docker system prune --force
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/common:latest -f common_utils/Dockerfile.common common_utils/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/common-chariots:latest -f ml_back/Dockerfile ml_back/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/cahriots-server:latest -f ml_back/k8/chariots_server/Dockerfile.server ml_back/k8/chariots_server/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/cahriots-workers:latest -f ml_back/k8/chariots_worker/Dockerfile.worker ml_back/k8/chariots_worker/
	DOCKER_BUILDKIT=1 docker build -t eu.gcr.io/chariots-poc/ml_back/redis-db:latest -f ml_back/k8/redis/Dockerfile.redis ml_back/k8/redis/

docker-push:
	docker push eu.gcr.io/chariots-poc/ml_back/common:latest
	docker push eu.gcr.io/chariots-poc/ml_back/common-chariots:latest
	docker push eu.gcr.io/chariots-poc/ml_back/cahriots-server:latest
	docker push eu.gcr.io/chariots-poc/ml_back/cahriots-workers:latest
	docker push eu.gcr.io/chariots-poc/ml_back/redis-db:latest
