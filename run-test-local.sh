#! /bin/bash

export PYTHONPATH=`pwd`/f8a_tagger/

function prepare_venv() {
    VIRTUALENV=`which virtualenv`
    if [ $? -eq 1 ]; then
        # python34 which is in CentOS does not have virtualenv binary
        VIRTUALENV=`which virtualenv-3`
    fi

    ${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt && python3 `which pip3` install -r test_requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

cd tests
PYTHONDONTWRITEBYTECODE=1 python3 `which pytest` --cov=../f8a_tagger/ --cov-report term-missing -vv .
