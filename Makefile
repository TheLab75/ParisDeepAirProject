################ PACKAGE ACTIONS ################

reinstall_package:
	@pip uninstall -y ParisDeepAirProject_install_package || :
	@pip install -e .

##################### API #####################
# API
run_api:
	uvicorn workflow.api:app --reload

# Test API
default:
	@echo 'tests are only executed locally for this challenge'

test_api: test_api_root test_api_predict

test_api_root:
	TEST_ENV=development pytest tests/api -k 'test_root' --asyncio-mode=strict -W "ignore"

test_api_predict:
	TEST_ENV=development pytest tests/api -k 'test_predict' --asyncio-mode=strict -W "ignore"

##################### DOCKER #####################
MULTI_REGION=eu.gcr.io
PROJECT=wagon-bootcamp-1002-365114
IMAGE=deepair
BUILD="${MULTI_REGION}/${PROJECT}/${IMAGE}"
docker_build:
	docker build --platform linux/amd64 -t ${BUILD} .

docker_run:
	docker run -e PORT=8000 -p 8080:8000 ${BUILD}

docker_push:
	docker push ${BUILD}

cloud_run_deploy:
	gcloud run deploy \
		--image ${BUILD} \
		--region europe-west9 \
		--memory 8Gi \
		--cpu 2
