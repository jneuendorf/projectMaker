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
            setter_name = convert_case("set_" + prop["name"]),
            getter_name = convert_case("get_" + prop["name"]),
            var_name    = prop["name"],
        )

    return res

def ctor_assignments(props, indentation):
    indentation = " " * indentation
    return "\n".join((indentation + "$this->" + prop["name"] + " = $" + prop["name"] + ";") for prop in props)




def create_code(config):

    model_template = string.Template("""
class $class_name implements DBModel {
$declare_properties

    public function __construct($properties) {
$ctor_assignments
    }

    // GETTERS & SETTERS
$define_getters_and_setters
}
""")


    # TODO: move code_style stuff to main (and accessibility here!)
    code_style = config["code_style"] if "code_style" in config else "snake"

    if code_style == "snake":
        def _convert_string(s):
            return string_to_snake_case(s)
        def _convert_case(s):
            return camel_to_snake_case(s)
    else:
        def _convert_string(s):
            return string_to_camel_case(s)
        def _convert_case(s):
            return snake_to_camel_case(s)

    global convert_string
    convert_string = _convert_string

    global convert_case
    convert_case = _convert_case





    for model_name in config["models"]:
        model_config = config["models"][model_name]
        # print(model_config)

        # prop_list = properties(model_config)


        model_code = model_template.substitute(
            class_name                  = snake_to_camel_case(model_name),
            declare_properties          = declare_properties(model_config, 4),
            properties                  = properties(model_config),
            ctor_assignments            = ctor_assignments(model_config, 8),
            define_getters_and_setters  = define_getters_and_setters(model_config, 4)
        )

        print(model_code)

        # TODO
        # code_file = open(config["title"] + "/app/models/" + model_name.lower() + ".php", "w")
        # code_file.write()
        # code_file.close()



    return 2
