#!/bin/bash


# create folders
cp -R ./data/file_structure asdf


# start code generation
python3 ./main.py $1 $2
