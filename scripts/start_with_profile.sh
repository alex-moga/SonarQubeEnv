#!/bin/bash

# Start SonarQube
./bin/run.sh &

LANGUAGE=java
PROFILE_NAME="Dit_java_qa_profile"
BASE_URL=http://127.0.0.1:9000

function isUp {
  curl -s -u admin:admin -f "$BASE_URL/api/system/info"
}

# Wait for server to be up
PING=`isUp`
while [ -z "$PING" ]
do
  sleep 5
  PING=`isUp`
done

# Perform post configuration of SonarQube
python ./bin/post_config_sonar.py $BASE_URL 

wait
