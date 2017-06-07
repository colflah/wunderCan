import mechanize, json, urllib, arrow

# STEP 1.1 -- get access token
#with open("../canvas_token",'r') as token_file:
#    token = token_file.read()
token = "5296~rJO92RTZgVb9WKIdaCr7TXde1xBGani0XP9xoFsBzbeXmjxOfA52P6260wkg1NhL"

# STEP 1.2 -- get classes and corresponding codes and put them in 'courses' list

br = mechanize.Browser()
response1 = br.open("https://nuevaschool.instructure.com/api/v1/users/self/favorites/courses?access_token="+token)
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

#for course in courses:
	#'context_codes[]':"course_"+course['ID']
# STEP 1.3 -- get assignments and add course name to them, store in 'assignments' list
query_params = {'type':'assignment','start_date':current_date,'end_date':future_date,'per_page':50,'access_token':token}
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
