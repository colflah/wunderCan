#!/bin/sh

git pull origin master
service nginx restart
service uwsgi restart
echo "service start"
