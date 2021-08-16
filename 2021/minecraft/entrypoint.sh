#!/bin/bash

loop () {
    while [ ! -f /app/logs/latest.log ]; do
        echo "Waiting for log file to exist"
        sleep 1
    done

    echo "Log file ready"

    tail --follow /app/logs/latest.log --retry 2>/dev/null | { 
        while read line; do
            echo $line | grep -P --color=none "^\[\d+:\d+:\d+ INFO\]: <RACTFAdmin> \!exec" | cut -d'!' -f2 | cut -d' ' -f2- | bash --restricted &
        done
        }
}

loop &

java -XX:+UseG1GC -Xms768m -Xmx768m -jar /app/paper.jar
