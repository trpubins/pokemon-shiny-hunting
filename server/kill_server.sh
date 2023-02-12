#!/bin/bash
pid=
pid=$(ps -ef | grep uvicorn | grep -v grep | awk '{print $2}')
kill -9 $pid
pid=
