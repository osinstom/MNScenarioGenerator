#!/bin/bash

LAUNCHER_DIR=/home/user/MNScenarioGenerator/
TOPOLOGY=
SCENARIO=

if [ -z "$1" ]; then
	echo "topology was not defined"
	exit -1
else

TOPOLOGY=$1

#splitting topology string into shell variables 
eval $(
	echo $TOPOLOGY | awk 'BEGIN {FS="-|:"}
	{
	print "TOPOLOGY_NAME="$1;
	print "LINK_BW="$2;
	print "HOST_DISTR="$3;
	print "HOSTS="$NF
	}'
      ) 

fi

if [ -z "$2" ]; then
	echo "scenario was not defined"
	exit -2
else


SCENARIO=$2
#splitting scenario string into shell variables
eval $(
	echo $SCENARIO | awk 'BEGIN {FS="_|-|:"}
	{
	print "TRAFFIC_GEN="$1;
	print "TRAFFIC_TYPE="$2;
	print "BR_MIN="$3;
	print "BR_MAX="$4;
	print "HOST_TRAFFIC_GEN="$5;
	print "HOST_FLOWS="$NF;
	}'
      ) 

fi

#TODO kill everything that is running

LOG_FILE="/home/user/Dropbox/CoSDN/mininet/log.txt"
STATUS_FILE="/home/user/Dropbox/CoSDN/mininet/status.txt"

##################TO DO############################
# Variables :
#
# TOPOLOGY_NAME, LINK_BW, HOST_DISTR, HOSTS,
# TRAFFIC_GEN,TRAFFIC_TYPE,BR_MIN,BR_MAX,HOST_TRAFFIC_GEN,HOST_FLOWS
#
#
# NOT USED :
# TRAFFIC_GEN (defult : iperf)
# HOST_DISTR

###################################################

CMD="$LAUNCHER_DIR/test_launcher_itg.py"
CMD+=" -t $TOPOLOGY_NAME"
CMD+=" -B $LINK_BW"
CMD+=" -H $HOSTS"

CMD+=" -T $TRAFFIC_TYPE"
CMD+=" --c_min $BR_MIN"
CMD+=" --c_max $BR_MAX"
CMD+=" -g $HOST_TRAFFIC_GEN"
CMD+=" -f $HOST_FLOWS"


#CMD+=" -s $SCENARIO"
#CMD+=" -d $LAUNCHER_DIR/scenarios"
CMD+=" -d $LAUNCHER_DIR/scenarios_link"
CMD+=" -l -o /home/user/Dropbox/CoSDN/mininet/logs"


echo "active" > $STATUS_FILE
echo "$CMD"
echo "$CMD" >> $LOG_FILE
$CMD >> $LOG_FILE
echo "result $?" >> $LOG_FILE
echo "idle" > $STATUS_FILE
