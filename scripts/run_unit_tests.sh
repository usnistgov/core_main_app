#!/bin/bash
SCRIPT_PATH=`dirname $0`
python -m unittest discover ${SCRIPT_PATH}/..
