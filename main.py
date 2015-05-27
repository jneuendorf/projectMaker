#!/usr/bin/python

import importlib
import os.path
import sys
import yaml



argv = sys.argv
argc = len(argv)


if argc <= 1:
    filename = "project.yml"
else:
    filename = argv[0]

# check for both .yaml and .yml version of filename (in case of typo)
if not os.path.isfile(filename):
    filename = filename.replace(".yml", ".yaml")

    if not os.path.isfile(filename):
        sys.exit(1)



config_file = open(filename, "r")
config_raw = config_file.read()
config_file.close()

config = yaml.load(config_raw)
# print(config)

language = config["language"] or "php"





module = importlib.import_module("data.languages." + language)
# print(dir(module))
module.create_code(config)
