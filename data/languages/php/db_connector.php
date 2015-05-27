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
        $this->domain   = $domain;
        $this->user     = $user;
        $this->pw       = $pw;
        $this->name     = $name;

        $this->mysqli   = new mysqli($domain, $user, $pw, $name);

        $this->connected = false;
    }

    public function connect() {
        // $this->mysqli = new mysqli($this->domain, $this->user, $this->pw, $this->name);

        if (!$this->connected) {
            // TODO: ??
            $htis->mysqli->open();

            if($this->mysqli->connect_errno != 0) {
                return false;
            }
            $this->connected = true;
        }
        return true;
    }

    public function disconnect()	{
        if ($this->connected) {
            if($this->mysqli->close()) {
                $this->mysqli = null;
                $this->connected = false;
                return true;
            }
        }
        return false;
    }

    public function is_connected() {
        return $this->connected === true;
    }

    public function query($query) {
        if ($this->connected) {
            return $this->mysqli->query($query);
        }
        return null;
    }

    public function force_query($query) {
        if ($this->connected) {
            return $this->mysqli->query($query);
        }
        else {
            $this->connect();
            $res = $this->mysqli->query($query);
            $this->disconnect();
            return $res;
        }
    }
}



?>
