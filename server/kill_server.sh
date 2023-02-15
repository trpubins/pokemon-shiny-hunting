#!/bin/bash
pid=
pid=$(ps -ef | grep uvicorn | grep -v grep | awk '{print $2}')
if [ "$pid" == "" ]; then
    echo "no uvicorn process to kill"
else
    echo "killing uvicorn process $pid"
    kill -9 $pid
fi
pid=
