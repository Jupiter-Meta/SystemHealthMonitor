#!/bin/bash

#script to keep running the performance test

while [ true ]; do
{
date
/home/pi/RPiHealth/performance.py
sleep 2
} >> /home/pi/performance.log
done
