.PHONY: help setup verify test docs book clean

PYTHON ?= .venv/bin/python

help:
	@echo "setup   Install the documentation and test dependencies"
	@echo "verify  Run source-integrity checks"
	@echo "test    Run all repository tests"
	@echo "docs    Build the website with warnings as errors"
	@echo "book    Build the Version 2 PDF"

setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r docs/requirements.txt -r requirements-dev.txt

verify:
	$(PYTHON) scripts/verify_content.py

test:
	$(PYTHON) -m pytest -q

docs:
	$(PYTHON) -m sphinx -W --keep-going -n -b html docs docs/_build/html

book:
	mkdir -p output/pdf
	latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=seqtec_v2 main.tex
	makeglossaries seqtec_v2
	latexmk -pdf -interaction=nonstopmode -halt-on-error -jobname=seqtec_v2 main.tex
	cp seqtec_v2.pdf output/pdf/seqtec_v2.pdf

clean:
	latexmk -C -jobname=seqtec_v2 main.tex
	rm -rf docs/_build
