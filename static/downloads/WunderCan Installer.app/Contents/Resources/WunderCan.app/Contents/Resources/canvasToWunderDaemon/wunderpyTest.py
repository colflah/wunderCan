import wunderpy2
from pprint import pprint

# establish acccess to wunderlist API using wunderpy2
api = wunderpy2.WunderApi()
access_token = "37abdca083dca429439f78b5aab67b410e19bd965be2a283d80bf2bf03d6" # this is MY access token. See https://pypi.python.org/pypi/wunderpy2/0.1.4 for info on getting access tokens for other users
client_id = "541ab1f4caa4896bb47d"
client = api.get_client(access_token,client_id)


#test getting all list
lists = client.get_lists()
pprint(lists)
#test getting list by name
aList=lists[0]
pprint(aList[wunderpy2.List.TITLE])
pprint(aList)

#test creating list
testList=client.create_list("TESTLIST")
#test creating task in testList
task = client.create_task(testList[wunderpy2.List.ID], "My new task", due_date="2015-03-26", starred=True)

#test creating note
client.create_note(task[wunderpy2.Task.ID], "My note")
#test creating subtask
client.create_subtask(task[wunderpy2.Task.ID], "My subtask")