import mechanize
from bs4 import BeautifulSoup
import urllib2
import cookielib
import time
import json
from pprint import pprint
import wunderpy2
import arrow


# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# PART 1 -- GETTING EVENTS OFF CALENDAR

# STEP 1.1 -- set up mechanize browser to login into canvas to get cookie
cj = cookielib.CookieJar() # creating cookie storage
br = mechanize.Browser()
br.set_cookiejar(cj) # setting cookie storage
br.open('https://nuevaschool.instructure.com/login/canvas')
br.select_form(nr=0)
br.form['pseudonym_session[unique_id]'] = 'colflah'
br.form['pseudonym_session[password]']='Welcome1'
br.submit()

# STEP 1.2 -- get classes and corresponding codes and put them in 'courses' list
response1 = br.open("https://nuevaschool.instructure.com/api/v1/users/self/favorites/courses?include[]=term&exclude[]=enrollments")
coursesJson = response1.read()
coursesJson = coursesJson.replace("while(1);","")
coursesJson = json.loads(coursesJson)
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
api_call = "https://nuevaschool.instructure.com/api/v1/calendar_events?type=assignment&context_codes%5B%5D=course_918&context_codes%5B%5D=course_827&context_codes%5B%5D=course_909&context_codes%5B%5D=course_876&context_codes%5B%5D=course_963&context_codes%5B%5D=user_88&context_codes%5B%5D=course_802&context_codes%5B%5D=course_888&start_date="+current_date+"T08%3A00%3A00.000Z&end_date="+future_date+"T07%3A00%3A00.000Z&per_page=50"
response2 = br.open(api_call)
classAssignments = response2.read()
classAssignments = classAssignments.replace("while(1);","")
classAssignments = json.loads(classAssignments)

assignments = []
for obj in classAssignments:
	assignmentName = obj[u'title']
	assignmentDueDate = str(obj[u'assignment'][u'due_at']).split("T")[0]
	assignmentCourseID = str(obj[u'assignment'][u'course_id'])
	assignmentCourseName = None
	for course in courses:
		if assignmentCourseID == course['ID']:
			assignmentCourseName = course['Name']
	assignment = {"Title": assignmentName,"Due Date":str(assignmentDueDate),"Course":str(assignmentCourseName)}
	assignments.append(assignment)

# assignments variable points to list of assignments to add.
# courses variable points to list of courses and their respective ID's.


# PART 2 -- UPDATING TO WUNDERLIST

# STEP 2.1 -- establish acccess to wunderlist API using wunderpy2
api = wunderpy2.WunderApi()
access_token = "37abdca083dca429439f78b5aab67b410e19bd965be2a283d80bf2bf03d6" # this is MY access token. See https://pypi.python.org/pypi/wunderpy2/0.1.4 for info on getting access tokens for other users
client_id = "541ab1f4caa4896bb47d"
client = api.get_client(access_token,client_id)

# STEP 2.2 -- establish access to MongoDB and define pointers to collections
from pymongo import MongoClient
connection = MongoClient('localhost', 27017)
db = connection['canvasToWunder']
db['Test'].insert_one({'Test':"Successful"})
courseCollections = []
for course in courses:
	course.update({'collection':db[course['Name'].replace(" ","").replace("-","")]})

# STEP 2.3 -- Delete assignments whose due date is prior to the current day
# On line 47, current date in Pacific time is assigned to current_date
for course in courses:
	for assignment in course['collection'].find():
		if assignment['Due Date'] < current_date:
			course['collection'].delete_one(assignment)

# STEP 2.3 -- add assignments to wunderlist 
wuLists = client.get_lists()
for assignment in assignments:
	listID = None
	for wuList in wuLists:
		if assignment["Course"]==str(wuList[u'title']):
			listID = wuList[u'id']
			# check if assignment has already been added to wunderlist
			for upAssignment in client.get_tasks(listID):
				if assignment['Title'] == upAssignment[u'title']:
					listID = None
			# check if assignment has been uploaded in the past but deleted from WunderList
			course = [course for course in courses if course['Name']==assignment['Course']]
			for upAssignment in course[0]['collection'].find():
				if upAssignment['Title']==assignment['Title']:
					listID = None
	if listID is not None:
		client.create_task(listID,assignment['Title'],due_date=assignment['Due Date'])
		course = [course for course in courses if course['Name']==assignment['Course']]
		course[0]['collection'].insert_one(assignment)





