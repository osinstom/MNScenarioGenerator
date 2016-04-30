#!/bin/bash

LAUNCHER_DIR=/home/user/MNScenarioGenerator/
TOPOLOGY=
SCENARIO=

if [ -z "$1" ]; then
	echo "topology was not defined"
	exit -1
else
	TOPOLOGY=$1
fi

if [ -z "$2" ]; then
	echo "scenario was not defined"
	exit -2
else
	SCENARIO=$2
fi

#TODO kill everything that is running

LOG_FILE="/home/user/Dropbox/CoSDN/mininet/log.txt"
STATUS_FILE="/home/user/Dropbox/CoSDN/mininet/status.txt"

CMD="$LAUNCHER_DIR/test_launcher_itg.py"
CMD+=" -t $TOPOLOGY"
CMD+=" -s $SCENARIO"
#CMD+=" -d $LAUNCHER_DIR/scenarios"
CMD+=" -d $LAUNCHER_DIR/scenarios_link"
CMD+=" -l -o /home/user/Dropbox/CoSDN/mininet/logs"
echo "active" > $STATUS_FILE
echo "$CMD"
echo "$CMD" >> $LOG_FILE
$CMD >> $LOG_FILE
echo "result $?" >> $LOG_FILE
echo "idle" > $STATUS_FILE
