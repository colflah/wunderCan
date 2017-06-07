How to Use:

1) Adjust values in scraperV2.py and intializeScraper.py:
	-Set password and username to your Canvas Password and UserName
	-Still need to implement feature to get other people’s access tokens (you 		can’t use this scraper until this feature is implemented)
2) initialize the Scraper:
	$ . venv/bin/activate
	$ python intializeScraper.py
3) run Mongo Daemon in background:
	$ mongod &
3) set up launchDaemon:
	$ chmod a+x canvasToWunderDaemonScript.sh
	-Copy personalScript.canvasToWunder.plist to ~/Library/LaunchDaemons/
		-Make sure path to canvasToWunderDaemonScript.sh in the plist file is 			correct

It will now update overtime you login.

----------------------------------------------------------------------------------------
TODO:

-Implement feature to get other people’s access tokens.

