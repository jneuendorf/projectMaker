import importlib
import os.path
from shell import shell
import string
import sys
import yaml

from lib import *



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




def shell_p(command):
    print(command)
    return shell(command)

def map_sql_type(generalType):
    generalType = generalType.lower()
    mapping = {
        "int":      "int",
        "integer":  "int",

        "string":   "varchar(1000)",

        "float":    "float",
        "double":   "double",
        "number":   "double",
        "real":     "double",

        "bool":     "tinyint(1)",
        "boolean":  "tinyint(1)",

        "date":     "date",
        "time":     "datetime",

        "array":    "varchar(100000)",
        "object":   "varchar(100000)"
    }

    return mapping[generalType] if generalType in mapping else mapping["string"]



def create_sql(model_config):
    sql_template = string.Template("""
--
-- Table structure for table `$table_name`
--

DROP TABLE IF EXISTS `$table_name`;

CREATE TABLE `$table_name` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
$table_props
    PRIMARY KEY (`id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- LOCK TABLES `$table_name` WRITE;
-- INSERT INTO `$table_name` VALUES (...), (...);
-- UNLOCK TABLES;
""")

    # `report_method` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `name_eng` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `name_deu` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `rollover_eng` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `rollover_deu` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `needs_authentication` tinyint(1) DEFAULT NULL,
    # `sequence` int(11) DEFAULT NULL,
    # `reportable_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `created_at` datetime NOT NULL,
    # `updated_at` datetime NOT NULL,
    # `precision` int(11) DEFAULT NULL,
    # `kpi_group_id` int(11) DEFAULT NULL,
    # `unit` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `aggregation` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
    # `category` text COLLATE utf8_unicode_ci,
    # `kind_id` int(11) DEFAULT NULL,
    # `kind_type` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,


    table_prop_template = string.Template("    `$col_name` $type COLLATE utf8_unicode_ci DEFAULT NULL,\n")

    result = {}
    sql = ""

    for model_name in model_config:
        model_props = model_config[model_name]

        table_props = ""

        for model_prop in model_props:
            if "plural" in model_prop:
                continue

            prop_name = model_prop["name"]
            prop_type = map_sql_type(model_prop["type"] if "type" in model_prop else "string")

            table_props = table_props + table_prop_template.substitute(
                col_name    = prop_name,
                type        = prop_type
            )

        table_name = table_name_for_model(model_name, model_config, False)

        result[table_name + ".sql"] = sql_template.substitute(
            table_name = table_name,
            table_props = table_props
        )



    return result



##################################################################################################################
# MAIN PROGRAM
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

if not os.path.exists("./data/jQuery/" + jquery_name + ".min.js"):
    shell_p("curl -o ./data/jQuery/" + jquery_name + ".min.js 'http://code.jquery.com/" + jquery_name + ".min.js'")
    shell_p("curl -o ./data/jQuery/" + jquery_name + ".js 'http://code.jquery.com/" + jquery_name + ".js'")

shell_p("cp ./data/jQuery/" + jquery_name + ".min.js '" + out_dir + "/js_includes/'")
shell_p("cp ./data/jQuery/" + jquery_name + ".js '" + out_dir + "/js_includes/'")


module = importlib.import_module("data.languages." + language)
code_data = module.create_code(config)


##################################################################################################################
# WRITE CODE FILES
for folder in code_data:
    code_dict = code_data[folder]
    if folder == "index":
        folder = "."

    for filename in code_dict:
        code = code_dict[filename]

        file = open(out_dir + "/" + folder + "/" + filename, "xt")
        file.write(code)
        file.close()

        print("........wrote " + filename)

    print("...." + folder + " done...")



##################################################################################################################
# WRITE SQL FILES
print("....creating sql files...")

# TODO
sql_data = create_sql(config["models"] if "models" in config else {})

for filename in sql_data:
    code = sql_data[filename]

    file = open(out_dir + "/sql/" + filename, "xt")
    file.write(code)
    file.close()

    print("........wrote " + filename)
