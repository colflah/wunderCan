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

# STEP 2 -- get classes and corresponding codes and put them in 'courses' list
br = mechanize.Browser()
response1 = br.open("https://nuevaschool.instructure.com/api/v1/users/self/favorites/courses?access_token="+canvas_token)
#coursesJson = response1.read()
coursesJson = json.loads(response1.read())
courses = []
for obj in coursesJson:
	try:
		courseName = obj[u'name']
		courseID = obj[u'id']
		course = {'Name':str(courseName),'ID':str(courseID)}
		courses.append(course)
	except KeyError as e:
		print "Key Error raised on element: "
		print obj

# STEP 3 -- establish acccess to wunderlist API using wunderpy2
api = wunderpy2.WunderApi()
with open(os.path.expanduser("~")+"/Library/Application Support/WunderCan/wunderlist_token.txt",'r') as token_file:
	wunderlist_token = token_file.read()
#wunderlist_token = "37abdca083dca429439f78b5aab67b410e19bd965be2a283d80bf2bf03d6" # this is MY access token. See https://pypi.python.org/pypi/wunderpy2/0.1.4 for info on getting access tokens for other users

client_id = "541ab1f4caa4896bb47d"
client = api.get_client(wunderlist_token,client_id)

# STEP 4 -- add courses to wunderlist as lists
for course in courses:
	client.create_list(course['Name'])

# Get user name and canvas id to create unique mLab Collection for them
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
for course in courses:
	user_collection.insert_one({'course':course['Name'].replace(" ","").replace("-",""),'user_id':user_collection_name,"assignments":[]})
