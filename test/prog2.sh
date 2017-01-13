#!/bin/bash

num=0
while :; do
    if [[ $num -lt 10 ]]; then
        echo "prog2 sleep 1s"
        sleep 1
        let num++
    else
        break
    fi
done
