import re
import string


# code_style = "snake case"

def snake_to_camel_case(s):
   return "".join(word.capitalize() for word in s.split("_"))

def camel_to_snake_case(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def string_to_camel_case(s):
    pass

def string_to_snake_case(s):
    pass

convert_string = None
convert_case = None






def declare_properties(props, indentation):
    res = ""
    indentation = " " * indentation
    # NOTE: '$$' escapes '$'
    template = string.Template(indentation + "// $type\n" + indentation + "$visibility $$$var_name;\n")

    for prop in props:
        res += template.substitute(
            type        = prop["type"] if "type" in prop else "...",
            visibility  = prop["visibility"] if "visibility" in prop else "protected",
            var_name    = prop["name"]
        )

    return res

def properties(props):
    return ", ".join("$" + prop["name"] for prop in props)

def define_getters_and_setters(props, indentation):
    res = ""
    indentation = " " * indentation

    template = string.Template(
        indentation + "public function $setter_name($$$var_name) {\n" +
        indentation + "    $$this->$var_name = $$$var_name;\n" +
        indentation + "    return $$this;\n\n" +
        indentation + "public function $getter_name() {\n" +
        indentation + "    return $$this->$$$var_name;\n" +
        indentation + "}\n\n"
    )

    for prop in props:
        res += template.substitute(
            # setter_name = convert_case("set_" + prop["name"]),
            # getter_name = convert_case("get_" + prop["name"]),
            setter_name = "set_" + prop["name"],
            getter_name = "get_" + prop["name"],
            var_name    = prop["name"],
        )

    return res

def define_find_methods(props, indentation):
    res = ""
    indentation = " " * indentation

    template = string.Template(
        indentation + "public static function find_by_$var_name($$$var_name) {\n" +
        indentation + "    return static::find_by(array(\"$var_name\" => $$$var_name));\n" +
        indentation + "}\n\n"
    )

    for prop in props:
        res += template.substitute(
            var_name = prop["name"]
        )

    return res

def ctor_assignments(props, indentation):
    indentation = " " * indentation
    return "\n".join((indentation + "$this->" + prop["name"] + " = $" + prop["name"] + ";") for prop in props)


def define_routes(routes, mode, indentation):
    route_template = string.Template("""if ($check_vars) {
    $$result = $output_pre;

    echo $output;
    exit(0);
}
""")

    # for data in routes:
    #     type    = data["type"]
    #     route   = data["to"]
    #     format  = "format" in data ? data["format"] : "string"
    #
    #     # parse route
    #     route_details = route.split("#")

    result  = """<?php
"""
    indentation = " " * indentation

    for type in routes:
        result = result + "\n// " + type.upper() + " REQUESTS\n"
        requrest_var = "$_" + type.upper()

        routes_data = routes[type]
        for route in routes_data:
            params = routes_data[route]

            format = "string"
            for param in params:
                if "format" in param:
                    format = param["format"]
                    params.remove(param)
                    break

            check_vars = " && ".join("isset(" + requrest_var + "[\"" + param + "\"])" for param in params)

            result += route_template.substitute(
                check_vars = check_vars,
                output_pre = "\"\"" if format == "string" else "array()",
                output = "$result" if format == "string" else "json_encode($result)"
            )

    print(result)

    return result



##################################################################################################################
##################################################################################################################
# MAIN FUNCTION!!                                                                                                #
##################################################################################################################

def create_code(config):

    db_connector_template = string.Template("""<?php

require_once "$connector_class.php";

$$db_connector = new $connector_class("$domain", "$user", "$password", "$db_name");

?>""")

    api_template = string.Template("""<?php
        $define_routes
?>""")

    model_template = string.Template("""<?php

require_once "../includes/init.php";
require_once "Model.php";

class $class_name extends AbstractDBModel {
$declare_properties

    public function __construct($properties) {
$ctor_assignments
    }

    // GETTERS & SETTERS
$define_getters_and_setters

    // STATIC
    // convenience find methods
$define_find_methods
}

$class_name::init($$db_connector, "$table_name");

?>""")

    if "database_connector" in config:
        if config["database_connector"].lower() == "mysqli":
            connector_class = "MySQLiDBConnector"
        elif config["database_connector"].lower() == "pdo":
            connector_class = "PDODBConnector"
    else:
        connector_class = "MySQLiDBConnector"


    db_connector_code = db_connector_template.substitute(
        connector_class = connector_class,
        domain      = config["database"]["domain"],
        user        = config["database"]["user"],
        password    = config["database"]["password"],
        db_name     = config["database"]["name"],
    )

    print("init.php:")
    print(db_connector_code)


    result = {
        "php_includes": {
            "init.php": db_connector_code
        },
        "index": {}, # top level files
        "models":   {}
    }


    # # TODO: move code_style stuff to main (and accessibility here!)
    # code_style = config["code_style"] if "code_style" in config else "snake"
    #
    # if code_style == "snake":
    #     def _convert_string(s):
    #         return string_to_snake_case(s)
    #     def _convert_case(s):
    #         return camel_to_snake_case(s)
    # else:
    #     def _convert_string(s):
    #         return string_to_camel_case(s)
    #     def _convert_case(s):
    #         return snake_to_camel_case(s)
    #
    # global convert_string
    # convert_string = _convert_string
    #
    # global convert_case
    # convert_case = _convert_case


    ##############################################################################################################
    # MODELS
    for model_name in config["models"]:
        model_config = config["models"][model_name]

        class_name = snake_to_camel_case(model_name)
        table_name = class_name + "s"

        for item in model_config:
            if "plural" in item:
                table_name = item["plural"]
                model_config.remove(item)
                break

        table_name = table_name.lower()

        model_code = model_template.substitute(
            class_name                  = class_name,
            declare_properties          = declare_properties(model_config, 4),
            properties                  = properties(model_config),
            ctor_assignments            = ctor_assignments(model_config, 8),
            define_getters_and_setters  = define_getters_and_setters(model_config, 4),
            define_find_methods         = define_find_methods(model_config, 4),
            table_name                  = table_name
        )

        # print(model_code)
        result["models"][model_name.lower() + ".php"] = model_code

    ##############################################################################################################
    # API
    if "routes" in config:
        routes_config = config["routes"]
        routing_mode = config["routing"] if "routing" in config else "simple"

        result["index"]["api.php"] = api_template.substitute(
            define_routes = define_routes(routes_config, routing_mode, 0)
        )

    return result
