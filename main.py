#!/usr/bin/python

import importlib
import os.path
from shell import shell
import sys
import yaml



argv = sys.argv
argc = len(argv)

# parse command line arguments
if argc <= 1:
    filename = "project.yml"
else:
    filename = argv[1]

if argc <= 2:
    out_dir = "."
else:
    out_dir = argv[2]




# check for both .yaml and .yml version of filename (in case of typo)
if not os.path.isfile(filename):
    filename = filename.replace(".yml", ".yaml")

    if not os.path.isfile(filename):
        print("No yaml file found (looked for '" + filename + "')! Exiting...")
        sys.exit(1)



config_file = open(filename, "r")
config_raw = config_file.read()
config_file.close()

config = yaml.load(config_raw)
# print(config)

project_name = config["title"]
language = config["language"] if "language" in config else "php"


# create folder structure
print("cp -R ./data/files '" + out_dir +  "/" + project_name + "'")
shell("cp -R ./data/files '" + out_dir +  "/" + project_name + "'")

out_dir = out_dir + "/" + project_name


module = importlib.import_module("data.languages." + language)
# print(dir(module))
data = module.create_code(config)

# write code files
for folder in data:
    code_dict = data[folder]
    if folder == "index":
        folder = "."

    for filename in code_dict:
        code = code_dict[filename]

        file = open(out_dir + "/" + folder + "/" + filename, "xt")
        file.write(code)
        file.close()
