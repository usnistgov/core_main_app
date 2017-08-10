#!/bin/bash
SCRIPT_PATH=`dirname $0`
python -m unittest discover ${SCRIPT_PATH}/../core_main_app -p "tests_unit*.py"