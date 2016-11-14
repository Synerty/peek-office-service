#!/usr/bin/env bash

. /etc/start_enmac.opt

HOME=/users/enmac

DIR=${HOME}/peek_client
AGENT_PYC="$DIR/run_peek_client.pyc"
PYTHON_HOME=${HOME}/python27

# Add the python paths
export PYTHONPATH=$DIR
export PATH=${PYTHON_HOME}/bin:$PATH

# Setup the envrionment for the python oracle library
export ORACLE_HOME=${PYTHON_HOME}/oracle/instantclient_11_2
export LD_LIBRARY_PATH=${ORACLE_HOME}

# Rotate Logs
LOG=$HOME/peek_client_pof.log
[ -f ${LOG}.1 ] && mv ${LOG}.1 ${LOG}.2
[ -f ${LOG} ] && mv ${LOG} ${LOG}.1

# Run python agent
python -u $AGENT_PYC >> $LOG 2>&1 &

