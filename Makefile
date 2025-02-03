SHELL := /bin/bash

all:
	@echo "There's no default Makefile target right now. Try:"
	@echo ""
	@echo "make clean - reset the project and remove auto-generated assets."
	@echo "make tidy - tidy up the code with the 'black' formatter."
	@echo "make lint - check the code for obvious errors with flake8."
	@echo "make lint-all - check all code for obvious errors with flake8."
	@echo "make serve - serve the project at: http://localhost:8000/"
	@echo "make widgets - generate the JSON definition of available widgets."
	@echo "make test - while serving the app, run the test suite in browser."
	@echo "make zip - create a zip archive of the framework and test suite."

clean:
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf py2blocks.tar.gz
	rm -rf test_suite.tar.gz
	rm -rf static/*.tar.gz
	rm -rf test_suite
	find . | grep -E "(__pycache__)" | xargs rm -rf

tidy:
	black -l 79 src tests utils

lint:
	flake8 --extend-ignore=E203,E701 src/*

lint-all:
	flake8 --extend-ignore=E203,E701 src/* tests/*

serve: clean tidy zip
	python utils/serve.py

test:
	python -m webbrowser http://localhost:8000/index.html

zip:
	cd src && tar --no-xattrs -czvf ../py2blocks.tar.gz *
	mkdir test_suite
	cp -r src/* test_suite
	cp -r tests test_suite
	cd test_suite && tar --no-xattrs -czvf ../test_suite.tar.gz tests/* *
	rm -rf test_suite
	cp py2blocks.tar.gz static/
	cp test_suite.tar.gz static/
	rm py2blocks.tar.gz
	rm test_suite.tar.gz

zip-all: lint-all clean tidy zip