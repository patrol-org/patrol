# This file is part of patrol, fork of range.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

NAME = patrol
VERSION = $(shell grep -m 1 -o '[0-9][0-9.]\+\S*' README.md)
NAME_RIFLE = rifle
VERSION_RIFLE = $(VERSION)
SNAPSHOT_NAME ?= $(NAME)-$(VERSION)-$(shell git rev-parse HEAD | cut -b 1-8).tar.gz
# Find suitable python version (need python >= 2.6 or 3.1):
PYTHON ?= $(shell \
	     (which python3) \
	     || (python -c 'import sys; sys.exit(sys.version < "2.6")' && \
	      which python) \
	     || (python2 -c 'import sys; sys.exit(sys.version < "2.6")' && \
	         which python2) \
	   )
ifeq ($(PYTHON),)
  $(error No suitable python found.)
endif
SETUPOPTS ?= '--record=install_log.txt'
DOCDIR ?= doc/pydoc
DESTDIR ?= /
PREFIX ?= /usr/local
PYOPTIMIZE ?= 1
FILTER ?= .

CWD = $(shell pwd)

bold := $(shell tput bold)
normal := $(shell tput sgr0)

default: test compile
	@echo 'Run `make options` for a list of all options'

options: help
	@echo
	@echo 'Options:'
	@echo 'PYTHON = $(PYTHON)'
	@echo 'PYOPTIMIZE = $(PYOPTIMIZE)'
	@echo 'DOCDIR = $(DOCDIR)'
	@echo 'DESTDIR = $(DESTDIR)'

help:
	@echo 'make:                 Test and compile patrol.'
	@echo 'make install:         Install $(NAME)'
	@echo 'make pypi_sdist:      Release a new sdist to PyPI'
	@echo 'make clean:           Remove the compiled files (*.pyc, *.pyo)'
	@echo 'make doc:             Create the pydoc documentation'
	@echo 'make cleandoc:        Remove the pydoc documentation'
	@echo 'make man:             Compile the manpage with "pod2man"'
	@echo 'make manhtml:         Compile the html manpage with "pod2html"'
	@echo 'make snapshot:        Create a tar.gz of the current git revision'
	@echo 'make test:            Test everything'
	@echo 'make test_pylint:     Test using pylint'
	@echo 'make test_flake8:     Test using flake8'
	@echo 'make test_doctest:    Test using doctest'
	@echo 'make test_pytest:     Test using pytest'
	@echo 'make test_other:      Verify the manpage is complete'
	@echo 'make test_py:         Run all python tests, including manpage completeness'
	@echo 'make test_shellcheck: Test using shellcheck'
	@echo 'make todo:            Look for TODO and XXX markers in the source code'

install:
	$(PYTHON) setup.py install $(SETUPOPTS) \
		'--prefix=$(PREFIX)' '--root=$(DESTDIR)' \
		--optimize=$(PYOPTIMIZE)

compile: clean
	PYTHONOPTIMIZE=$(PYOPTIMIZE) $(PYTHON) -m compileall -q patrol

clean:
	find patrol -regex .\*\.py[co]\$$ -delete
	find patrol -depth -name __pycache__ -type d -exec rm -r -- {} \;

doc: cleandoc
	mkdir -p $(DOCDIR)
	cd $(DOCDIR); \
		$(PYTHON) -c 'import pydoc, sys; \
		sys.path[0] = "$(CWD)"; \
		pydoc.writedocs("$(CWD)")'
	find . -name \*.html -exec sed -i 's|'"$(CWD)"'|../..|g' -- {} \;

TEST_PATHS_MAIN = \
	$(shell find ./patrol -mindepth 1 -maxdepth 1 -type d \
		! -name '__pycache__' \
		! -path './patrol/config' \
		! -path './patrol/data' \
	) \
	./patrol/__init__.py \
	$(shell find ./doc/tools ./examples -type f -name '*.py') \
	./patrol.py \
	./setup.py \
	./tests
TEST_PATH_CONFIG = ./patrol/config

test_pylint:
	@echo "$(bold)Running pylint...$(normal)"
	pylint $(TEST_PATHS_MAIN)
	pylint --rcfile=$(TEST_PATH_CONFIG)/.pylintrc $(TEST_PATH_CONFIG)

test_flake8:
	@echo "$(bold)Running flake8...$(normal)"
	flake8 $(TEST_PATHS_MAIN) $(TEST_PATH_CONFIG)
	@echo

test_doctest:
	@echo "$(bold)Running doctests...$(normal)"
	@set -e; \
	for FILE in $(shell grep -IHm 1 doctest -r patrol | grep $(FILTER) | cut -d: -f1); do \
		echo "Testing $$FILE..."; \
		PATROL_DOCTEST=1 PYTHONPATH=".:"$$PYTHONPATH ${PYTHON} $$FILE; \
	done
	@echo

test_pytest:
	@echo "$(bold)Running py.test tests...$(normal)"
	py.test tests
	@echo

test_py: test_pylint test_flake8 test_doctest test_pytest test_other
	@echo "$(bold)Finished python and documentation tests!$(normal)"
	@echo

test_shellcheck:
	@echo "$(bold)Running shellcheck...$(normal)"
	sed '2,$$s/^\([[:blank:]]*\)#/\1/' ./patrol/data/scope.sh \
	| shellcheck -a -
	@echo

test_other:
	@echo "$(bold)Checking completeness of man page...$(normal)"
	@tests/manpage_completion_test.py
	@echo

test: test_py test_shellcheck
	@echo "$(bold)Finished testing: All tests passed!$(normal)"

doc/patrol.1: doc/patrol.pod
	pod2man --stderr --center='patrol manual' \
		--date='$(NAME)-$(VERSION)' \
		--release=$(shell date -u '+%Y-%m-%d') \
		doc/patrol.pod doc/patrol.1

doc/rifle.1: doc/rifle.pod
	pod2man --stderr --center='rifle manual' \
		--date='$(NAME_RIFLE)-$(VERSION_RIFLE)' \
		--release=$(shell date -u '+%Y-%m-%d') \
		doc/rifle.pod doc/rifle.1

man: doc/patrol.1 doc/rifle.1

manhtml:
	pod2html doc/patrol.pod --outfile=doc/patrol.1.html

cleandoc:
	test -d $(DOCDIR) && rm -- $(DOCDIR)/*.html || true

snapshot:
	git archive --prefix='$(NAME)-$(VERSION)/' --format=tar HEAD | gzip > $(SNAPSHOT_NAME)

dist: snapshot

todo:
	@grep --color -Ion '\(TODO\|XXX\).*' -r patrol

.PHONY: clean cleandoc compile default dist doc help install man manhtml \
	options snapshot test test_pylint test_flake8 test_doctest test_pytest \
	test_other todo pypi_sdist
