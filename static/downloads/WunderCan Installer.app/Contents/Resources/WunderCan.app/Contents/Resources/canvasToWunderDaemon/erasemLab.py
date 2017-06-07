import mechanize
from bs4 import BeautifulSoup
import urllib2
import cookielib
import time
import json
from pprint import pprint
import wunderpy2
import os
import ast
import requests
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# setting working directory to this file's directory
os.chdir("/Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon")

# STEP 1 -- get access token
with open(os.path.expanduser("~")+"/Library/Application Support/WunderCan/canvas_refresh_token.txt",'r') as token_file:
    canvas_refresh_token = token_file.read()
# use refresh token to get access token
url = "https://nuevaschool.instructure.com/login/oauth2/token"
payload = {'grant_type':'refresh_token','client_id':'52960000000000002','client_secret':'I5TXjoH4cG2bUbDuYYEKloVguAftsTpXE4aILIZIxVXKXenZHGlF4GG3rdhyVcre','refresh_token':canvas_refresh_token}
headers = {'content-type':'application/json'}
canvas_token = ast.literal_eval(requests.post(url,data=json.dumps(payload),headers=headers).content)['access_token']
#canvas_token = "5296~rJO92RTZgVb9WKIdaCr7TXde1xBGani0XP9xoFsBzbeXmjxOfA52P6260wkg1NhL"


# Get user name and canvas id to create unique mLab Collection for them
br = mechanize.Browser()
user_request = br.open("https://nuevaschool.instructure.com/api/v1/users/self/profile?access_token="+canvas_token)
userInfo = json.loads(user_request.read())
user_name = str(userInfo['name'])
user_id = str(userInfo['id'])

user_collection_name = user_name.replace(" ","")+user_id # This will be unique name of mLab collection that stores users assignments

# STEP 5 -- create mLab collection for user
from pymongo import MongoClient
connection = MongoClient('mongodb://wundercanco:wunderwunder@ds111882.mlab.com:11882/wundercan')
db = connection['wundercan']
user_collection = db[user_collection_name]
user_collection.delete_many({})
