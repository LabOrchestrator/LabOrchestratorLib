build:
	rm -Rf dist/*
	python3 -m build

push:
	python3 -m twine upload --repository testpypi dist/*

install-dev:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine
