
coffee:
	coffee --output data/files/js_includes --compile data/unprocessed/coffee


compile: coffee

run: compile
	# sh main.sh
	python3 main.py
