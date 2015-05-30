<?php

require_once "../data/languages/php/Model.php";
require_once "../data/languages/php/MySQLiDBConnector.php";
require_once "../data/languages/php/PDODBConnector.php";

$db_connector = new MySQLiDBConnector("localhost", "root", "", "test");
// $db_connector = new PDODBConnector("localhost", "root", "", "test");

/**
 *
 */
class Record extends AbstractDBModel {

    protected $name;
    protected $data;

    public function __construct($data) {
        parent::__construct($data);
    }

}

Record::init($db_connector);

var_dump(Record::get_columns());

$record = new Record(array(
    "name" => "test_name",
    "data" => "{\"a\": 10, \"b\": 20}"
));
print_r($record);

echo "<br><br>";
print_r($record->get_attributes());
// var_dump((new ReflectionClass("Record"))->find(1));

echo "<br><br>";

// echo Record::get_class_name();
// echo $record->get_class_name()."<br>\n";

echo "Record::all()<br>";
print_r(Record::all());

echo "<br><br>";
print_r(Record::all(true));

echo "<br><br>";
echo Record::count();

echo "<br>find...<br><br>";
print_r(Record::find(1));

echo "<br><br>";
print_r(Record::find_by(array("name" => "first one")));
echo "<br>";
print_r(Record::find_by(array("data" => "some awesome data")));
echo "<br>";
print_r(Record::find_by(array("id" => 1)));
echo "<br>";
print_r(Record::find_by(array("id" => 42)));

echo "<br><br>";


$record->save();

$db_connector->disconnect();



?>
<!DOCTYPE html>
<html>
    <head>
        <title>PHP-Test</title>

        <script type="text/javascript" src=""></script>

        <link rel="stylesheet" href="/css/master.css" media="screen" title="no title" charset="utf-8">
    </head>
    <body>
        <div class="header"></div>
        <div class="content"></div>
        <div class="footer"></div>
    </body>
</html>
