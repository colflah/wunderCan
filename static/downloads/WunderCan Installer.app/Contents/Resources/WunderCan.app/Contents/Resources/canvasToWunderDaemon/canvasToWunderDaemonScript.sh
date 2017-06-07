#!/bin/sh
( id -a

   pwd

  /bin/ls -dlaeO@ .

   echo $#

   echo $0

  echo "$@"

   printenv

) >/tmp/my_launchd_environment.txt
cd /Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon
. venv27/bin/activate
python scraperWithCanvasApi.py
deactivate
