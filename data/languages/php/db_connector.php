<?php

class DBConnector {

    // string
    private $domain;
    private $user;
    private $pw;
    private $name;

    // mysqli
    private $mysqli;

    // boolean
    private $connected;

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // CONSTRUCTOR
    function __construct($domain, $user, $pw, $name) {
        $this->domain       = $domain;
        $this->user         = $user;
        $this->pw           = $pw;
        $this->name         = $name;

        // $this->mysqli       = null;
        $this->mysqli = new mysqli($domain, $user, $pw, $name);

        $this->connected    = false;
    }

    public function connect() {
        // $this->mysqli = new mysqli($this->domain, $this->user, $this->pw, $this->name);
        // TODO: ??
        $htis->mysqli->open();

        if($this->mysqli->connect_errno != 0) {
            return false;
        }

        $this->connected = true;
        return true;
    }

    public function disconnect()	{
        if($this->mysqli->close()) {
            $this->mysqli = null;
            $this->connected = false;
            return true;
        }

        return false;
    }

}



?>
