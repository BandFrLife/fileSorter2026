TYPE_CHECK   := --strict --allow-untyped-decorators --ignore-missing-imports
COVERAGE     := coverage
PROGRAM      := gui2.py
PYTHON       := python3
COMPILE      := python3
STYLE_CHECK  := flake8
FORMAT_CHECK := autopep8 --in-place --aggressive --recursive
MYPY         := mypy
TEST_ARGS    := -s --verbose --color=yes
PLANTUML     := plantuml
UML_DIR      := uml
PYTEST       := pytest
DOCS         := docs
TEST         := unittest
SRC_DIR      := src
TEST_DIR     := tests
TEST_FILE    := tests/test_*.py

.DEFAULT_GOAL = help

.PHONY: run
run:
	$(COMPILE) ./$(SRC_DIR)/$(PROGRAM)

.PHONY: all-checks
all-checks: check-format check-type check-style

.PHONY: check-type
check-type:
	$(MYPY) $(TYPE_CHECK) $(SRC_DIR) $(TEST_DIR)

.PHONY: check-format
check-format:
	$(FORMAT_CHECK) $(SRC_DIR)/ $(TEST_DIR)/

.PHONY: check-style
check-style:
	$(STYLE_CHECK) $(SRC_DIR) $(TEST_DIR)

.PHONY: create-docs
create-docs:
	mkdir -p $(DOCS)
	pdoc $(SRC_DIR)/ --output-dir $(DOCS)

# Generate UML images
.PHONY: create-uml
create-uml:
	$(PLANTUML) $(UML_DIR)/*.plantuml

.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache

.PHONY: run-test-coverage
run-test-coverage:
	PYTHONPATH=. $(PYTHON) -m $(COVERAGE) run -m $(PYTEST) -s $(TEST_DIR)/*.py -v
	$(PYTHON) -m $(COVERAGE) report -m

.PHONY: run-tests
run-tests: run-unittest run-pytest

.PHONY: run-unittest
run-unittest:
	PYTHONPATH=. $(COMPILE) -m $(TEST) discover -s $(TEST_DIR) -v

.PHONY: run-pytest
run-pytest:
	PYTHONPATH=. $(PYTEST) -s $(TEST_DIR) -v

.PHONY: allow-docker-gui
allow-docker-gui:
	xhost +local:docker

.PHONY: docker
docker: allow-docker-gui
	bash ./run-docker.sh

.PHONY: create-random-files
create-random-files:
	bash ./make_random_files.sh

.PHONY: clean-dirs
clean-dirs:
	# remove all caches recursively
	rm -rf `find . -type d -name '20*'` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache

## Show available Makefile commands
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make                      - Make help"
	@echo "  make run                  - run program"
	@echo "  make docker               - Creates a container and enters it"
	@echo "  make all-checks           - check type, style, format"
	@echo "  make check-type           - Run mypy on .py files"
	@echo "  make check-style          - lint files"
	@echo "  make check-format         - autopep8"
	@echo "  make run-test-coverage:   - Run pytest with report"
	@echo "  make create-random-files: - Add random files for testing"
	@echo "  make help                 - Display this menu"
	@echo "  make create-uml           - Generate .svg from .puml"
	@echo "  make clean                - Remove unnecesary py files/dirs"

