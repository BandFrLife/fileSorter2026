PROGRAM = gui.py
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
	find . -type d -name "__pycache__" -exec rm -r {} +

## Show available Makefile commands
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make               - Make help"
	@echo "  make help          - Display this menu"
	@echo "  make create-uml    - Generate .svg from .puml"
	@echo "  make clean         - Remove __pycache__ files"

