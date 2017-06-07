import mechanize
from bs4 import BeautifulSoup
import urllib2
import cookielib
import time
import json
from pprint import pprint
import wunderpy2
import arrow
import urllib
import os
import requests
import ast


# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# setting working directory to this file's directory
os.chdir("/Applications/WunderCan.app/Contents/Resources/canvasToWunderDaemon")

# PART 1 -- GETTING EVENTS OFF CALENDAR

# STEP 1.1 -- get access token
with open(os.path.expanduser("~")+"/Library/Application Support/WunderCan/canvas_refresh_token.txt",'r') as token_file:
    canvas_refresh_token = token_file.read()
# use refresh token to get access token
url = "https://nuevaschool.instructure.com/login/oauth2/token"
payload = {'grant_type':'refresh_token','client_id':'52960000000000002','client_secret':'I5TXjoH4cG2bUbDuYYEKloVguAftsTpXE4aILIZIxVXKXenZHGlF4GG3rdhyVcre','redirect_uri':'http://wundercan.tk/authorize/canvas/init','refresh_token':canvas_refresh_token}
headers = {'content-type':'application/json'}
#canvas_token = ast.literal_eval(requests.post(url,data=json.dumps(payload),headers=headers).content)['access_token']

#For testing purposes:
canvas_token = "5296~rJO92RTZgVb9WKIdaCr7TXde1xBGani0XP9xoFsBzbeXmjxOfA52P6260wkg1NhL"

# STEP 1.2 --s get classes and corresponding codes and put them in 'courses' list

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


# PRE-STEP1.3 -- get current date and date 28 days from now

current_date = arrow.utcnow().to('US/Pacific').format('YYYY-MM-DD')
future_date = arrow.utcnow().to('US/Pacific').replace(weeks=+4).format('YYYY-MM-DD')

# STEP 1.3 -- get assignments and add course name to them, store in 'assignments' list
query_params = {'type':'assignment','start_date':current_date,'end_date':future_date,'per_page':50,'access_token':canvas_token}
url = "https://nuevaschool.instructure.com/api/v1/calendar_events?"
api_call = url+urllib.urlencode(query_params)
for course in courses:
    api_call=api_call+'&context_codes[]=course_'+course['ID']
response2 = br.open(api_call)
classAssignments = response2.read()
classAssignments = json.loads(classAssignments)


assignments = []
for obj in classAssignments:
    assignmentName = obj[u'title']
    assignmentDueDate = str(obj[u'assignment'][u'due_at']).split("T")[0]
    assignmentCourseID = str(obj[u'assignment'][u'course_id'])
    assigmentDescription = str(obj[u'description'])
    assignmentCourseName = None
    for course in courses:
        if assignmentCourseID == course['ID']:
            assignmentCourseName = course['Name']
    assignment = {"Title": assignmentName,"Due Date":str(assignmentDueDate),"Course":str(assignmentCourseName),"Description":str(assigmentDescription)}
    assignments.append(assignment)

# assignments variable points to list of assignments to add.
# courses variable points to list of courses and their respective ID's.


# PART 2 -- UPDATING TO WUNDERLIST

# STEP 2.1 -- establish acccess to wunderlist API using wunderpy2
api = wunderpy2.WunderApi()
with open(os.path.expanduser("~")+"/Library/Application Support/WunderCan/wunderlist_token.txt",'r') as token_file:
    wunderlist_token = token_file.read()
#wunderlist_token = "37abdca083dca429439f78b5aab67b410e19bd965be2a283d80bf2bf03d6" # this is MY access token. See https://pypi.python.org/pypi/wunderpy2/0.1.4 for info on getting access tokens for other users
client_id = "541ab1f4caa4896bb47d"
client = api.get_client(wunderlist_token,client_id)

# Get user name and canvas id to create unique mLab Collection for them
user_request = br.open("https://nuevaschool.instructure.com/api/v1/users/self/profile?access_token="+canvas_token)
userInfo = json.loads(user_request.read())
user_name = str(userInfo['name'])
user_id = str(userInfo['id'])

user_collection_name = user_name.replace(" ","")+user_id # This will be unique name of mLab collection that stores users assignments

# I NEED TO UPDATE 2.2,2.3 WITH ACCESS TO MLABS, SEE CODE ON OTHER COMPUTER
# STEP 2.2 -- establish access to MongoDB and define pointers to collections
from pymongo import MongoClient
connection = MongoClient('mongodb://wundercanco:wunderwunder@ds111882.mlab.com:11882/wundercan')
db = connection['wundercan']
user_collection = db['user_collection_name']
for course in courses:
    course.update({'doc':db[user_collection_name].find_one({'course':course['Name'].replace(" ","").replace("-","")})})

# STEP 2.3 -- Delete assignments whose due date is prior to the current day
# On line 47, current date in Pacific time is assigned to current_date
for course in courses:
    for assignment in course['doc']['assignments']:
        if assignment['Due Date'] < current_date:
            user_collection.update(course['doc'],{'$pull':{'assignments.Title':assignment['Title']}})

# STEP 2.3 -- add assignments to wunderlist
wuLists = client.get_lists()
for assignment in assignments:
    listID = None
    for wuList in wuLists:
        if assignment["Course"]==str(wuList[u'title']):
            listID = wuList[u'id']
            # check if assignment has already been added to wunderlist
            for upAssignment in client.get_tasks(listID):
                if assignment['Title'] == str(upAssignment[u'title']):
                    listID = None
            # check if assignment has been uploaded in the past but deleted from WunderList
            course = [course for course in courses if course['Name']==assignment['Course']]
            for upAssignment in course[0]['doc']['assignments']:
                if upAssignment['Title']==assignment['Title']:
                    listID = None
    if listID is not None:
        task = client.create_task(listID,assignment['Title'],due_date=assignment['Due Date'])
        try:
            client.create_note(task[wunderpy2.Task.ID],assignment["Description"])
        except Exception as e:
            print(e)
        course = [course for course in courses if course['Name']==assignment['Course']]
        user_collection.update(course[0]['doc'],{'$push':assignment})
