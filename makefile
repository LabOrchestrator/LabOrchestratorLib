build:
	rm -Rf dist/*
	python3 -m build

push_testing:
	python3 -m twine upload --repository testpypi dist/*

push:
	python3 -m twine upload --repository pypi dist/*

install-dev:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine
