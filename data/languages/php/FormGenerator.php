<?php

require_once "models/require_all.php";


class FormGenerator {

    protected static $closingTags;
    protected static $standardElementDefs;
    protected static $typeToElementMapping;


    public static function init() {
        static::$closingTags = array(
            "textarea"
        );

        static::$standardElementDefs = array(
            "textfield" => array(
                "tag"   => "input",
                "type"  => "text",
                "class" => "textfield"
            ),
            "integerfield" => array(
                "tag"   => "input",
                "type"  => "number",
                "step"  => 1,
                "class" => "integerfield"
            ),
            "floatfield" => array(
                "tag"   => "input",
                "type"  => "number",
                "step"  => 0.1,
                "class" => "floatfield"
            ),
            "textarea" => array(
                "tag"   => "textarea",
                "class" => "textarea"
            )
        );

        static::$typeToElementMapping = array(
            "integer"   => static::$standardElementDefs["integerfield"],
            "float"     => static::$standardElementDefs["floatfield"],
            "string"    => static::$standardElementDefs["textfield"],

            "boolean"   => array(
                0 => array(
                    "tag" => "input",
                    "type" => "radio",
                    "value" => "0"
                ),
                1 => array(
                    "tag" => "input",
                    "type" => "radio",
                    "value" => "1"
                )
            ),

            "array"     => static::$standardElementDefs["textarea"],
            "object"    => static::$standardElementDefs["textarea"]
        );
    }

    protected static function createElement($name, $type, $options=array()) {
        $order  = array("tag", "type", "id", "class", "value");
        $data   = static::$typeToElementMapping[$type];
        $result = "<";

        if (!isset($options["name"])) {
            $options["name"] = $name;
        }

        // do attributes defined in $order
        for ($i = 0; $i < count($order); $i++) {
            $attr = $order[$i];
            if (isset($options[$attr])) {
                if ($attr !== "tag") {
                    $result .= $attr."=\"".$options[$attr]."\" ";
                }
                else {
                    $result .= $options[$attr]." ";
                }
            }
            elseif (isset($data[$attr])) {
                if ($attr !== "tag") {
                    $result .= $attr."=\"".$data[$attr]."\" ";
                }
                else {
                    $result .= $data[$attr]." ";
                }
            }
        }

        // do remaining attributes
        foreach ($options as $attr => $value) {
            $result .= $attr."=\"".$value."\" ";
        }

        // close element tag
        if (in_array($data["tag"], static::$closingTags)) {
            $result .= "></".$data["tag"].">";
        }
        else {
            $result .= "/>";
        }

        return $result;
    }

    public static function makeFor($model, $output=NULL) {
        var_dump("generating forms!!");

        // model instance given =>
        if (!is_string($model)) {
            $model = get_class($model);
        }

        // NOTE: from http://stackoverflow.com/questions/3354628/from-the-string-name-of-a-class-can-i-get-a-static-variable
        // for newer versions of PHP (5.3+)
        try {
            $column_names = $model::get_columns();
            $column_types = $model::get_types();
        }
        // for older versions of PHP
        catch (Exception $e) {
            $column_names = (new ReflectionProperty($model, "get_columns"))->invoke(NULL);
            $column_types = (new ReflectionProperty($model, "get_types"))->invoke(NULL);
        }

        echo "<br><br>";

        $result = "<form action=\"\" method=\"post\">\n".
                  "    <input type=\"hidden\" name=\"id\" />\n";

        for ($i = 0; $i < count($column_names); $i++) {
            $name = $column_names[$i];
            $type = $column_types[$i];
            if ($i === 0) {
                $options = array("tabindex" => 0);
            }
            else {
                $options = array();
            }
            $result .= "    <span class=\"label\">".$name.":</span>\n".
                       "    ".static::createElement($name, $type)."<br />\n";
        }

        $result .= "    <button type=\"submit\">Submit</button>\n".
                   "</form>";

        echo $result;

    }
}

FormGenerator::init();

?>
