################ PACKAGE ACTIONS ################

reinstall_package:
	@pip uninstall -y ParisDeepAirProject_install_package || :
	@pip install -e .

##################### TESTS #####################



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
