import re
import string

from lib import *


def snake_to_camel_case(s):
   return "".join(word.capitalize() for word in s.split("_"))

def camel_to_snake_case(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def string_to_camel_case(s):
    pass

def string_to_snake_case(s):
    pass

def read_file(filename):
    file = open(filename, "r")
    result = file.read()
    file.close()
    return result

def map_type(generalType):
    generalType = generalType.lower()
    mapping = {
        "int":      "integer",
        "integer":  "integer",

        "string":   "string",

        "double":   "float",
        "float":    "float",
        "number":   "float",
        "real":     "float",

        "bool":     "boolean",
        "boolean":  "boolean",

        "date":     "integer",
        "time":     "integer",

        "array":    "array",
        "object":   "object"
    }

    return mapping[generalType] if generalType in mapping else "string"





def declare_properties(props, indentation):
    res = ""
    indentation = " " * indentation
    # NOTE: '$$' escapes '$'
    template = string.Template(indentation + "// $type\n" + indentation + "$visibility $$$var_name;\n")

    for prop in props:
        print(prop)
        res += template.substitute(
            type        = map_type(prop["type"]) if "type" in prop else "...",
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
        indentation + "    return $$this;\n" +
        indentation + "}\n\n" +
        indentation + "public function $getter_name() {\n" +
        indentation + "    return $$this->$$$var_name;\n" +
        indentation + "}\n\n"
    )

    for prop in props:
        res += template.substitute(
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
    return """<?php

function delegate_route($route) {
    if (isset($_GET[$route])) {
        $req_type = "get";
    }
    elseif (isset($_POST[$route])) {
        $req_type = "post";
    }
    else {
        echo "{\\"error\\": \\"Call to undefined route!\\", \\"route\\": \\"".$route."\\"}";
        exit(0);
    }

    require_once "api/".$route.".php";

    if ($api_controller->check_route($route, $req_type)) {
        $api_controller->$route($_GET);
        exit(0);
    }
}

?>"""

def make_api_files(routes):
    api_file_template = string.Template("""<?php

// called from api.php (included from there) => go from api.php's path
if (file_exists("controllers/ApiController.php")) {
    require_once "controllers/ApiController.php";
}
// called from here => go from here
else {
    require_once "../controllers/ApiController.php";
}

$$api_controller = new ApiController();

if ($check_vars) {
    $assign_vars

    // output format: $format
    echo $output;
}

?>""")

    result = {}

    for type in routes:
        request_var = "$_" + type.upper()

        routes_data = routes[type]
        for route in routes_data:
            params = dict(routes_data[route])

            if "format" not in params:
                format = "string"
            else:
                format = params["format"]
                del params["format"]


            check_vars = " && ".join("isset(" + request_var + "[\"" + param + "\"])" for param in params)

            api_controller_call = "$api_controller->" + route + "(array(" + (", ".join("\"" + param + "\" => $" + param for param in params)) + "))"

            print(api_controller_call)

            result[route + ".php"] = api_file_template.substitute(
                check_vars = check_vars,
                assign_vars = "\n    ".join("$" + param + " = (" + map_type(params[param]) + ") " + request_var + "[\"" + param + "\"];" for param in params),
                format = format,
                output = api_controller_call if format == "string" else "json_encode(" + api_controller_call + ")"
            )

    return result


def make_api_controller(routes):
    controller_template = string.Template("""<?php

// require_once "../models/require_all.php";

class ApiController {

    private $$route_types = array(
        $route_types
    );

    public function __construct() {

    }

    public function route_is_valid($$route, $$type) {
        return isset($$this->route_types[$$type]);
    }

$define_controller_functions

}

?>""")

    func_template = string.Template("""
    public function $func_name($$params) {
$assign_vars

        $$result = $pre_output;

        return $$result;
    }
""")

    funcs = ""
    route_types = {}
    route_types_keys = []

    for type in routes:
        routes_data = routes[type]
        for route in routes_data:
            route_types[route] = type.lower()
            route_types_keys.append(route)

            params = dict(routes_data[route])

            if "format" not in params:
                format = "string"
            else:
                format = params["format"]
                del params["format"]

            assign_vars = ""
            for param in params:
                assign_vars = assign_vars + "        $" + param + " = $params[\"" + param + "\"];\n"

            funcs = funcs + func_template.substitute(
                func_name = route,
                assign_vars = assign_vars,
                pre_output = "\"\"" if format == "string" else "array()"
            )

    route_types_keys.sort()

    return controller_template.substitute(
        route_types = ",\n        ".join("\"" + route + "\" => \"" + route_types[route] + "\"" for route in route_types_keys),
        define_controller_functions = funcs
    )

def make_navigation(views, indentation):
    indentation = " " * indentation
    result = ""

    for view in views:
        result = result + (indentation + "<div class=\"item\">\n" +
                          indentation + "    <a href=\"index.php?view=" + view + "\">" + view + "</a>\n" +
                          indentation + "</div>\n")

    return result

##################################################################################################################
##################################################################################################################
# MAIN FUNCTION!!                                                                                                #
##################################################################################################################

def create_code(config):

    index_template = string.Template("""<?php

// session_start();
require_once "includes/functions.php";

// TODO: ENTER DEFAULT VIEW HERE!
$$default_view = "home";

if (isset($$_REQUEST["view"])) {
    $$view = $$_REQUEST["view"];
}
else {
    $$view = $$default_view;
}

?>
<!DOCTYPE html>
<html>
    <?php
        require_once "views/head.php";
    ?>
    <body>
        <div id="page">
            <div id="header">
                <div class="navigation">
$navigation
                </div>
            </div>

            <div id="content">
                <?php
                    if (file_exists("views/".$$view.".php")) {
                        require_once "views/".$$view.".php";
                    }
                    else {
                        require_once "views/".$$default_view.".php";
                    }
                ?>
            </div>

            <div id="footer"></div>
        </div>
    </body>
</html>
""")

    db_connector_template = string.Template("""<?php

require_once "$connector_class.php";

$$db_connector = new $connector_class("$domain", "$user", "$password", "$db_name");

?>""")

    model_template = string.Template("""<?php

require_once "includes/init.php";
require_once "includes/Model.php";

class $class_name extends AbstractDBModel {
$declare_properties

    // array
    protected static $$_column_names = array($column_names);
    // array
    protected static $$_column_types = array($column_types);

    public function __construct($properties) {
        parent::__construct();
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

    result = {
        "api":          {},
        "controllers":  {},
        "includes":     {
            "init.php":                 db_connector_code,
            "DBConnector.php":          read_file("./data/languages/php/DBConnector.php"),
            "MySQLiDBConnector.php":    read_file("./data/languages/php/MySQLiDBConnector.php"),
            "PDODBConnector.php":       read_file("./data/languages/php/PDODBConnector.php"),
            "Model.php":                read_file("./data/languages/php/Model.php"),
            "functions.php":            """<?php
// define your functions here
?>"""
        },
        "index":    {}, # top level files
        "models":   {},
        "views":    {}
    }

    ##############################################################################################################
    # INDEX.PHP



    result["index"]["index.php"] = index_template.substitute(
        navigation = make_navigation(config["views"] if "views" in config else {}, 24)
    )

    ##############################################################################################################
    # MODELS
    for model_name in config["models"]:
        model_config = config["models"][model_name]

        class_name = snake_to_camel_case(model_name)
        # table_name = model_name + "s"
        #
        # for item in model_config:
        #     if "plural" in item:
        #         table_name = item["plural"]
        #         model_config.remove(item)
        #         break

        table_name = table_name_for_model(model_name, model_config).lower()

        model_code = model_template.substitute(
            class_name                  = class_name,
            declare_properties          = declare_properties(model_config, 4),
            properties                  = properties(model_config),
            column_names                = ", ".join("\"" + item["name"] + "\"" for item in model_config),
            column_types                = ", ".join("\"" + (map_type(item["type"]) if "type" in item else "string") + "\"" for item in model_config),
            ctor_assignments            = ctor_assignments(model_config, 8),
            define_getters_and_setters  = define_getters_and_setters(model_config, 4),
            define_find_methods         = define_find_methods(model_config, 4),
            table_name                  = table_name
        )

        result["models"][class_name.lower() + ".php"] = model_code

    require = "<?php\n\n"
    for model_file_name in result["models"]:
        require = require + "require_once \"" + model_file_name + "\";\n"

    require = require + "\n ?>"


    result["models"]["require_all.php"] = require

    ##############################################################################################################
    # API (=api.php + files in api folder) (+ CONTROLLER)
    if "routes" in config:
        routes_config = config["routes"]
        routing_mode = config["routing"] if "routing" in config else "simple"

        result["index"]["api.php"] = define_routes(routes_config, routing_mode, 0)

        result["api"] = make_api_files(routes_config)

        result["controllers"]["ApiController.php"] = make_api_controller(routes_config)

    ##############################################################################################################
    # CONTROLLERS
    if "controllers" in config:
        controllers = config["controllers"]
        for controller in controllers:
            result["controllers"][controller + ".php"] = """<?php

require_once "models/require_all.php";

?>"""

    require = "<?php\n\n"
    for controller_name in result["controllers"]:
        require = require + "require_once \"" + controller_name + "\";\n"

    require = require + "\n ?>"


    result["controllers"]["require_all.php"] = require

    ##############################################################################################################
    # VIEWS
    result["views"]["head.php"] = string.Template("""<?php

?>
<!-- STYLESHEETS -->
<link rel="stylesheet" type="text/css" media="screen" href="css/general.css" />
<link rel="stylesheet" type="text/css" media="screen" href="css/header.css" />
<link rel="stylesheet" type="text/css" media="screen" href="css/content.css" />
<link rel="stylesheet" type="text/css" media="screen" href="css/footer.css" />

<!-- JAVASCRIPT -->
<script type="text/javascript" src="js_includes/$jquery_name.min.js"></script>
<script type="text/javascript" src="js_includes/Router.js"></script>

""").substitute(
        jquery_name = config["jQuery_name"]
    )

    if "views" in config:
        views = config["views"]
        for view in views:
            result["views"][view + ".php"] = """<?php

require_once "controllers/require_all.php";

?>"""

    return result
