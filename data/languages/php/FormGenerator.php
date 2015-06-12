<?php

require_once "models/require_all.php";


class FormGenerator {

    function __construct() {
        # code...
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

        var_dump($column_names);
        var_dump($column_types);

        echo "<br><br>";

    }
}


?>
