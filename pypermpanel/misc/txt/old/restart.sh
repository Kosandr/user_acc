#!/bin/bash

#sudo pkill python

#export FLASK_APP=serv.py
#python3 -m flask run --host=0.0.0.0 --port=4219 &

echo "previous proc `cat proc.pid`"
proc=`cat proc.pid` #$(echo `cat proc.pid` '+1' | bc)
echo "killing $proc"
#sudo kill -9  $proc
sudo kill -9 $proc
sleep 4
#sudo python3 serv.py &
#gunicorn serv:app --workers=5 --bind=4220

#sudo gunicorn serv:app --workers=5 -b 127.0.0.1:4220 -w3 --certfile=/etc/letsencrypt/live/familyape.com/fullchain.pem --keyfile=/etc/letsencrypt/live/familyape.com/privkey.pem &
gunicorn serv:app --workers=5 -b 127.0.0.1:4220 -w3 --certfile=/etc/letsencrypt/live/familyape.com/fullchain.pem --keyfile=/etc/letsencrypt/live/familyape.com/privkey.pem &

latest=$!
echo $latest >proc.pid
echo "curr proc: $latest"
#-export FLASK_APP=serv.py
#-python -m flask run --host=0.0.0.0 --port=6016
