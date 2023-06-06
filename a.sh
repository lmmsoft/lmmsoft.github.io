#!/bin/bash

rm -rf /tmp/speed_test
mkdir -p /tmp/speed_test
TIMEFORMAT="%R"

first_execution_time=0
second_execution_time=0

for i in {1..100};do
    FILENAME=$(openssl rand -hex 10)
    echo $'#!/bin/sh\necho Hello' > "/tmp/speed_test/$FILENAME.sh"
    chmod a+x "/tmp/speed_test/$FILENAME.sh"
    FILE="/tmp/speed_test/$FILENAME.sh"

    first=`(time $FILE > /dev/null) 2>&1`
    first_execution_time=$(echo "$first_execution_time + $first" | bc)

    second=`(time $FILE > /dev/null) 2>&1`
    second_execution_time=$(echo "$second_execution_time + $second" | bc)
done

echo "First time execution: $first_execution_time"
echo "Second time execution: $second_execution_time"