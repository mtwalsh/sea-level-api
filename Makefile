.PHONY: clean
clean: clean_python_bytecode

.PHONY: clean_python_bytecode
clean_python_bytecode:
	find . -iname '*.pyc' -exec rm {} +
	find . -iname '__pycache__' -type d -exec rm -rf {} +

