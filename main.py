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




def shell_p(command):
    print(command)
    return shell(command)


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

project_name = config["title"]
language = config["language"] if "language" in config else "php"

out_dir = out_dir + "/" + project_name

# create folder structure
shell_p("cp -R ./data/files '" + out_dir + "'")

# get jQuery
jquery_name = "jquery-" + config["jQuery"]
config["jQuery_name"] = jquery_name

if not os.path.isdir("./data/jQuery/" + jquery_name):
    shell_p("curl -o ./data/jQuery/" + jquery_name + ".min.js 'http://code.jquery.com/" + jquery_name + ".min.js'")
    shell_p("curl -o ./data/jQuery/" + jquery_name + ".js 'http://code.jquery.com/" + jquery_name + ".js'")

shell_p("cp ./data/jQuery/" + jquery_name + ".min.js '" + out_dir + "/js_includes/'")
shell_p("cp ./data/jQuery/" + jquery_name + ".js '" + out_dir + "/js_includes/'")


module = importlib.import_module("data.languages." + language)
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

    print("..." + folder + " done...")
