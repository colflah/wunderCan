#!/bin/sh

cd /Applications/Wundercan.app/Contents/Resources/canvasToWunderDaemon
. venv27/bin/activate
python initializeScraper.py
deactivate
