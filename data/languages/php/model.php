<?php

// interface DBModel {
//
//     // ACTIVE-RECORD CLASS METHODS
//     // public function self::all();
//     // public function create();
//
//     // ACTIVE-RECORD INSTANCE METHODS
//     public function save();
//     public function upsert();
//
//     public function find();
//     public function find_by();
//     public function where();
//
//     // CONNECTOR METHODS
//     public function set_db_connector();
//     public function get_db_connector();
// }

abstract class AbstractDBModel {

    // string
    public static final $name = "";

    private $id;
    // DBConnector
    private $db_connector;
    // boolean
    private $persistent;


    // ACTIVE-RECORD CLASS METHODS
    // public function AbstractDBModel::all() {}
    // public function create() {}
    // public function find() {
    //
    // }
    //
    // public function find_by() {
    //
    // }
    //

    /**
 	 * @param condition {string}
	 */
    public function where($condition) {
        $records = $this->db_connector->force_query("SELECT * FROM ".(self::name)." WHERE ".$condition.";")
        $res = arrya();
        for ($i = 0; $i < count($records); $i++) {
            array_push($res, );
        }
        return $res;
    }


    // CONSTRUCTOR
    public function __construct($db_connector=null) {
        $this->db_connector = $db_connector;
        // NOTE: if persistent is supposed to be true use AbstractDBModel::create()
        $this->persistent   = false;
    }


    // GETTERS & SETTERS
    public function set_db_connector($db_connector) {
        $this->db_connector = $db_connector;
        return $this;
    }

    public function get_db_connector() {
        return $this->db_connector;
    }

    public function set_persistent($persistent) {
        $this->persistent = $persistent;
        return $this;
    }

    public function is_persistent() {
        return $this->persistent === true;
    }

    public function get_persistent() {
        return $this->is_persistent();
    }



    // ACTIVE-RECORD INSTANCE METHODS
    /**
     * save record to database leaving the connector unchanged
     */
    public function save() {
        // already in DB => update
        if ($this->persistent) {
            $this->db_connector->force_query("INSERT INTO ".(self::$name)." VALUES WHERE id = ".$this->id.";");
        }
        // no in DB => insert
        else {
            $this->db_connector->force_query("UPDATE ".(self::name)." SET WHERE id = ".$this->id.";");
        }
    }

    // public function upsert() {
    //
    // }


}

?>
