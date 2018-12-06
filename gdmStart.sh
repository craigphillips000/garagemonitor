#!/bin/sh
python $HOME/gdm/doorSensor.py &
python $HOME/gdm/logMonitor.py &
python $HOME/gdm/actionEngine.py &
