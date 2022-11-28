################ PACKAGE ACTIONS ################

reinstall_package:
	@pip uninstall -y ParisDeepAirProject_install_package || :
	@pip install -e .

##################### TESTS #####################
