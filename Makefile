#
# Makefile (for developers)
#

.PHONY: coverage
coverage:
	pytest --cov dokang

.PHONY: coverage-html
coverage-html:
	pytest --cov dokang --cov-report html
	python -c "import webbrowser; webbrowser.open('htmlcov/index.html')"

.PHONY: test
test:
	pytest

.PHONY: docs
docs:
	SPHINXOPTS="-W -n" $(MAKE) -C docs html

.PHONY: quality
quality:
	isort --check-only --diff .
	pylint --reports=no --score=no setup.py dokang tests
	check-branches
	check-fixmes
	check-manifest
	python setup.py sdist >/dev/null 2>&1 && twine check dist/*

.PHONY: clean
clean:
	rm -rf .coverage
	find . -name "*.pyc" | xargs rm -f
	find . -name "__pycache__" | xargs rm -rf
	$(MAKE) -C docs clean
