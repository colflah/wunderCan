#!/bin/sh
echo "Moving WunderCan to /Applicationsdd"
cp -R WunderCan.app /Applications/
#sudo cp -R "../../../../WunderCan.app" "/Applications"
echo "Inititalizing LaunchDaemon"
cd /Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon
#sudo easy_install pip
#pip install virtualenv
virtualenv --python=python venv27
echo "made virtual env"
source venv27/bin/activate
echo "inside virtual env"
pip install -r requirements.txt
echo "installing requirements"
python initializeScraper.py
echo "running intit scraper"
deactivate
echo "deactivating scraper"
echo "Installing LaunchDaemon"
chmod a+x /Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon/canvasToWunderDaemonScript.sh
chmod a+x /Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon/initinit.sh
cp -R /Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon/wunderCanCo.canvasToWunder.plist /Library/LaunchAgents
cd ~
mkdir "Library/Application Support/WunderCan"
chown $(printenv USER) "Library/Application Support/WunderCan"
cd "Library/Application Support/WunderCan"
touch wunderlist_token.txt
touch canvas_token.txt
touch canvas_refresh_token.txt
open /Applications/WunderCan.app
open /Applications/WunderCan.app/Contents/Resources/WundercanInit.app