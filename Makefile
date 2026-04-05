PROGRAM = gui2.py
COMPILE = python3
PLANTUML     = plantuml
UML_DIR      = uml

.DEFAULT_GOAL = help

.PHONY: run
run:
	$(COMPILE) ./guiFiles/$(PROGRAM)


# Generate UML images
.PHONY: create-uml
create-uml:
	$(PLANTUML) $(UML_DIR)/*.plantuml -tsvg

.PHONY: clean
clean:
	# remove all caches recursively
	rm -rf `find . -type d -name __pycache__` # remove all pycache
	rm -rf `find . -type d -name .pytest_cache` # remove all pytest cache
	rm -rf `find . -type d -name .mypy_cache` # remove all mypy cache
	rm -rf `find . -type d -name .hypothesis` # remove all hypothesis cache
	rm -rf `find . -name .coverage` # remove all coverage cache

## Show available Makefile commands
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make               - Make help"
	@echo "  make run           - run program"
	@echo "  make help          - Display this menu"
	@echo "  make create-uml    - Generate .svg from .puml"
	@echo "  make clean         - Remove unnecesary py files/dirs"

