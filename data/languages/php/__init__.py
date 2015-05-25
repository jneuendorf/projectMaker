import string


code_style = "snake case"

def to_camel_case(s):
   return "".join(word.capitalize() for word in s.split("_"))


def declare_properties(props, indentation):
    res = ""

    indentation = " " * indentation
    for prop in props:
        res += (
            indentation + "// " + (prop["type"] if "type" in prop else "...") + "\n" +
            indentation + (prop["visibility"] if "visibility" in prop else "protected") +
            " $" + prop["name"] + ";\n"
        )

    return res

def properties(props):
    return ", ".join("$" + prop["name"] for prop in props)





def create_code(config):

    model_template = string.Template("""
    class $name implements DBModel {
$declare_properties

        public function __construct($properties) {

        }
    }
    """)


    for model_name in config["models"]:
        model_config = config["models"][model_name]
        # print(model_config)

        prop_list = properties(model_config)

        declared_properties = declare_properties(model_config, 8)



        print(model_template.substitute(
            name = to_camel_case(model_name),
            declare_properties = declared_properties,
            properties = prop_list
        ))

    return 2
