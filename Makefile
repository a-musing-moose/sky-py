test:
	py.test --pep8 --clearcache --cov sky tests

unit-test:
	py.test --pep8 --clearcache --cov sky tests/unit

initegration-tests:
	py.test --pep8 --clearcache --cov sky tests/integration

develop:
	pip install -e .
	pip install -r requirements.txt

travis: develop test

docs:
	cd docs; make html

.PHONY: test unit-test integration-test develop docs
