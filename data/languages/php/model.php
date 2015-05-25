<?php

interface DBModel {

    public function create();

    public function save();

    public function find();

    public function upsert();

}

?>
