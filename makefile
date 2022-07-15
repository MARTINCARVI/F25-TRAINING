test:
	venv/bin/python manage.py test --keepdb --parallel --exclude-tag slow --testrunner utils.tests.FastTestRunner

test-coverage:
	venv/bin/coverage run manage.py test --keepdb --parallel --exclude-tag slow --testrunner utils.tests.FastTestRunner
	venv/bin/coverage html

test-verbose:
	venv/bin/python -Wa manage.py test --keepdb
