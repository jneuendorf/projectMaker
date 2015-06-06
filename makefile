
coffee:
	coffee --output data/files/js_includes --compile data/unprocessed/coffee


compile: coffee

clean:
	rm -R 'My Project'

run: clean compile
	python3 main.py
