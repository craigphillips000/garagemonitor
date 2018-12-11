#!/bin/sh
python $HOME/gdm/doorSensor.py &
echo "doorSensor.py Starting"
sleep 5
python $HOME/gdm/logMonitor.py &
echo "logMonitor.py Starting"
sleep 5
python $HOME/gdm/actionEngine.py &
echo "actionEngine.py Starting"
