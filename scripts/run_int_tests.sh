#!/bin/bash
SCRIPT_PATH=`dirname $0`
python -m unittest discover ${SCRIPT_PATH}/.. -p "tests_int*.py"
