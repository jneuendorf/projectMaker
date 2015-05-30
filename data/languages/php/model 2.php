<?php


define("SERVER", "127.0.0.1");
define("USER", "root");
define("PASSWORD", NULL);
define("DATABASE", '');



/**
* Database connection class
* condtructor requires constants from config.php
* class dbquery extends parent class dbconnect
* methods of dbquery returns fetched arrays of a database query
 */
class PDODatabase
{
	static private $instance=NULL;

	static public function getInstance()
	{
		if(self::$instance===NULL)
		{
			try
			{
				self::$instance = new PDO('mysql:host='.SERVER.';dbname='.DATABASE, USER, PASSWORD,array(PDO::ATTR_ERRMODE=> PDO::ERRMODE_EXCEPTION,PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES utf8'));
			}
			catch (PDOException $e)
			{
				echo die('Keine Verbindung möglich.');
			}
		}
		return self::$instance;
	}

	private function __construct(){}

	static public function close()
	{
		self::$instance=null;
	}
}

class dbconnect{

	function __construct(){

		$this->connection = mysql_connect(SERVER, USER, PASSWORD,TRUE)
			or die ("Keine Verbindung m&ouml;glich. Benutzername oder Passwort sind falsch");
		mysql_set_charset("utf8", $this->connection);

		$selectDB = mysql_select_db(DATABASE,$this->connection)
			or die ("Die Datenbank `". DATABASE ."` existiert nicht.");
	}

	function close(){
		mysql_close();
	}
}


class dbquery extends dbconnect{

	public function query($query){
		$get_query=@mysql_query($query);
		$row = mysql_fetch_array($get_query);
		if(!$row)							// Kein Wert gefunden
			$row = NULL;
		return $row;
	}

	public function query_ar($query){
		$rows = array();
		$get_query=@mysql_query($query);
		while($row = mysql_fetch_array($get_query))
			$rows[] = $row;
		return $rows;
	}

	public function query_num($query){
		$get_query=@mysql_query($query);
		$numOf = mysql_num_rows($get_query);
		return $numOf;
	}

	public function show_query($query){
		echo $query;
	}


	#	Eingabe						//
	public function insert($tbl,$names,$values){
		$set_query=@mysql_query("INSERT INTO ".$tbl." (".$names.") VALUES (".$values.")");
		$id=mysql_insert_id();
		return $id;
	}

	public function show_insert($tbl,$names,$values){
		echo "INSERT INTO ".$tbl." (".$names.") VALUES (".$values.")";
	}

	#	Aenderung					//
	public function edit($tbl,$names,$values,$where){
		$set_query=@mysql_query("UPDATE ".$tbl." SET ".$names." = '".mysql_real_escape_string($values)."' WHERE ".$where);
		if($set_query)
			return "Daten geändert";
		else
			return "Änderung fehlgeschlagen";
	}

	#	Aenderung					//
	public function edit_unlimited($tbl,$changes,$where){
		$set_query=@mysql_query("UPDATE ".$tbl." SET ".$changes." WHERE ".$where);
		if($set_query)
			return "Daten geändert";
		else
			return "Änderung fehlgeschlagen";
	}

	public function show_edit($tbl,$names,$values,$where){
		echo "UPDATE ".$tbl." SET ".$names." = '".$values."' WHERE ".$where;
	}

	public function show_edit_unlimited($tbl,$changes,$where){
		echo "UPDATE ".$tbl." SET ".$changes." WHERE ".$where;
	}

	#	LOESCHEN					//
	public function delete($tbl,$where){
		$set_query=@mysql_query("DELETE FROM ".$tbl." WHERE ".$where);
		if($set_query)
			return "Daten gelöscht";
		else
			return "Löschung fehlgeschlagen";
	}

	public function show_delete($tbl,$where){
		echo "DELETE FROM ".$tbl." WHERE ".$where;
	}

}







class Model {

  static $id_col = "id";

  function __construct($id=null, $attrs=null) {
    $this->table = strtolower(get_called_class());
    $this->columns = $this->get_columns();
    $this->id = intval($id);
    $this->id_col = static::$id_col;

    if ($attrs !== null) {
      foreach ($this->columns as $col) {
        $this->attributes[$col["Field"]] = $attrs[$col["Field"]];
      }
    } else {
      if ($id !== null) {
        $this->attributes = $this->get_attributes();
      } else {
        $this->attributes = array();
      }
    }
  }

  function save() {
    $db=PDODatabase::getInstance();
    $params = "";
    foreach ($this->columns as $idx => $col) {
      if ($col["Field"] != $this->id_col) {
        $params .= $col["Field"] . "=:" . $col["Field"] . ",";
      }
    }
    $params = rtrim($params, ",");
    if ($this->id === null) {
      $statement = $db->prepare("INSERT INTO $this->table SET " . $params);
    } else {
      $statement = $db->prepare("UPDATE $this->table SET " . $params . " WHERE $this->id_col=:id");
      $statement->bindParam(":id", $this->id, PDO::PARAM_INT);
    }
    foreach ($this->columns as $idx => $col) {
      if ($col["Field"] != $this->id_col) {
        if ($this->get($col["Field"]) !== null) {
          $statement->bindParam(":".$col["Field"], $this->get($col["Field"]), PDO::PARAM_STR);
        } else {
          $statement->bindParam(":".$col["Field"], $this->get($col["Field"]), PDO::PARAM_NULL);
        }
      }
    }
    $statement->execute();
    if ($this->id === null) {
      $this->id = $db->lastInsertId();
    }
  }

  function get($attr) {
    return $this->attributes[$attr];
  }
  function set($attr, $val) {
    if (in_array($attr, $this->col_names())) {
      $this->attributes[$attr] = $val;
    }
  }

  function col_names() {
    return array_map(function($col) {return $col["Field"];}, $this->columns);
  }

  static function get_columns() {
    $table = strtolower(get_called_class());
    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SHOW FULL COLUMNS from $table");
    $statement->execute();
    return $statement->fetchAll();
  }

  function get_attributes() {
    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SELECT * from $this->table WHERE $this->id_col=:id");
    $statement->bindParam(":id", $this->id, PDO::PARAM_INT);
    $statement->execute();
    $attrs = $statement->fetchAll();
    $attrs = $attrs[0];
    $attributes = array();
    foreach ($this->columns as $col) {
      $attributes[$col["Field"]] = $attrs[$col["Field"]];
    }
    return $attributes;
  }

  static function count() {
    $table = strtolower(get_called_class());
    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SELECT count(*) from $table");
    $statement->execute();
    $r = $statement->fetchAll();
    return $r[0][0];
  }

  static function find($id) {
    $table = strtolower(get_called_class());
    $id_col = static::$id_col;
    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SELECT * from $table WHERE $id_col=:id");
    $statement->bindParam(":id", $id, PDO::PARAM_INT);
    $statement->execute();
    $result = $statement->fetchAll();
    $result = $result[0];
    $cls = (new ReflectionClass(get_called_class()));
    return $cls->newInstanceArgs(array($result["id"], $result));
  }

  static function find_by($attrs) {
    $cls = get_called_class();
    $table = strtolower(get_called_class());

    $params = "";
    foreach (static::get_columns() as $idx => $col) {
      if (isset($attrs[$col["Field"]])) {
        $params .= $col["Field"] . "=:" . $col["Field"] . " AND ";
      }
    }
    $params = rtrim($params, " AND ");

    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SELECT * from $table WHERE $params");
    foreach (static::get_columns() as $idx => $col) {
      if (isset($attrs[$col["Field"]])) {
        $statement->bindParam(":".$col["Field"], $attrs[$col["Field"]], PDO::PARAM_STR);
      }
    }
    $statement->execute();
    return array_map(function($el) use ($cls) {
      $cls = (new ReflectionClass($cls));
      return $cls->newInstanceArgs(array($el["id"], $el));
    }, $statement->fetchAll());
  }

  static function where($where, $parameters) {
    $cls = get_called_class();
    $table = strtolower($cls);

    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SELECT * from $table WHERE " . $where);
    foreach ($parameters as $key => $val) {
      $statement->bindParam($key, $parameters[$key], PDO::PARAM_STR); // for some reason, using $val doesn't work
    }
    $statement->execute();

    return array_map(function($el) use ($cls) {
      $rcls = (new ReflectionClass($cls));
      return $rcls->newInstanceArgs(array($el["id"], $el));
    }, $statement->fetchAll());
  }

  static function all() {
    $cls = get_called_class();
    $table = strtolower(get_called_class());

    $db=PDODatabase::getInstance();
    $statement = $db->prepare("SELECT * from $table");
    $statement->execute();
    return array_map(function($el) use ($cls) {
      $cls = (new ReflectionClass($cls));
      return $cls->newInstanceArgs(array($el["id"], $el));
    }, $statement->fetchAll());
  }
}

?>
