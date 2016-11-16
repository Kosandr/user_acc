#!/bin/bash

num_workers=5
ip=127.0.0.1
port=4220


echo "killin proc: `cat proc.pid`"

kill -9 `cat proc.pid`
sleep 6

ssl_data1=--certfile=/etc/letsencrypt/live/familyape.com/fullchain.pem

ssl_data2=--keyfile=/etc/letsencrypt/live/familyape.com/privkey.pem

gunicorn serv:app --workers=$num_workers -b $ip:$port -w3  $ssl_data1 $ssl_data2 &
latest=$!
echo $latest >proc.pid
echo "starting proc: $latest"

