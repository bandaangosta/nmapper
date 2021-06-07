all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf build #&& rm -rf *.log*

venv:
	python3 -m venv venv && venv/bin/pip install -e .

run: venv
	venv/bin/python -m nmapper

test: venv
	venv/bin/python -m unittest discover -s tests

build:
	python3 setup.py sdist bdist_wheel