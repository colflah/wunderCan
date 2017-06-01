#!bin/bash

. venv/bin/activate
sudo stop wunderCan
sudo start wunderCan
sudo service nginx restart

