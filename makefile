VERSION := $(shell python3 setup.py --version)


pypi-build:
	rm -Rf dist/*
	python3 -m build

pypi-push-testing:
	python3 -m twine upload --repository testpypi dist/*

pypi-push:
	python3 -m twine upload --repository pypi dist/*

install-dev:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine

git-tag:
	git tag "v$(VERSION)"

git-release:
	git push
	git push --tags

release: git-tag git-release pypi-build pypi-push
