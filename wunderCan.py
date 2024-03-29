import os
from flask import Flask, redirect, render_template, request
import ast
import requests
import json

application = Flask(__name__)

@application.route('/')
def home():
	return render_template('index.html')

# IGNORE THIS PATH
@application.route('/auth')
def auth():

	#code = "testcode"
	code=request.args.get('code')
	#state=request.args.get('state')


	#exchange code for access token, assign to token variable
	url = 'https://www.todoist.com/oauth/access_token'
        payload = {'client_id':'384c0e4c54944eb9ab951f345cbcff9f','client_secret':'30e67a1fdf464ac7aedb2cfa9b37c077','code':code}
        headers = {'content-type':'application/json'}
	#token ="test"
        token = requests.post(url,data=json.dumps(payload),headers=headers).content
	print(token)
	return redirect("ToDoAuth://",code=302)

@application.route('/authorize/canvas')
def authC():
	code=request.args.get('code')

	# exchange code for access token
	url = 'https://nuevaschool.instructure.com/login/oauth2/token'
	payload = {'grant_type':'authorization_code','client_id':'52960000000000002','client_secret':'I5TXjoH4cG2bUbDuYYEKloVguAftsTpXE4aILIZIxVXKXenZHGlF4GG3rdhyVcre','redirect_uri':'http://wundercan.tk/authorize/canvas','code':code}
	headers = {'content-type':'application/json'}
	aResponse = requests.post(url,data=json.dumps(payload),headers=headers).content
	with open("response.txt",'w') as file:
		file.write(aResponse)
	canvasAccessToken = ast.literal_eval(aResponse)['access_token']
	refreshToken = ast.literal_eval(aResponse)['refresh_token']

	return redirect("ToDoAuth://?type=canvas&token="+canvasAccessToken+"&refresh_token="+refreshToken, code=302)

@application.route('/authorize/canvas/init')
def authCInit():
	code=request.args.get('code')

	# exchange code for access token
	url = 'https://nuevaschool.instructure.com/login/oauth2/token'
	payload = {'grant_type':'authorization_code','client_id':'52960000000000002','client_secret':'I5TXjoH4cG2bUbDuYYEKloVguAftsTpXE4aILIZIxVXKXenZHGlF4GG3rdhyVcre','redirect_uri':'http://wundercan.tk/authorize/canvas/init','code':code}
	headers = {'content-type':'application/json'}
	aResponse = requests.post(url,data=json.dumps(payload),headers=headers).content
	with open("response.txt",'w') as file:
		file.write(aResponse)
	canvasAccessToken = ast.literal_eval(aResponse)['access_token']
	refreshToken = ast.literal_eval(aResponse)['refresh_token']

	return redirect("ToDoAuthInit://?type=canvas&token="+canvasAccessToken+"&refresh_token="+refreshToken, code=302)

@application.route('/authorize/wunder')
def authw():
 	code=request.args.get('code')

 	url = 'https://www.wunderlist.com/oauth/access_token'
 	payload = {'client_id':'541ab1f4caa4896bb47d','client_secret':'9c3fad36181643f1cbc80d8ef3d3dbaa57fe279bb1e6c7b03021d81d99f2','code':code}
 	headers = {'content-type':'application/json'}
 	wunderAccessToken = ast.literal_eval(requests.post(url,data=json.dumps(payload),headers=headers).content)['access_token']

	return redirect("ToDoAuth://?type=wunderlist&token="+wunderAccessToken, code=302)

@application.route('/authorize/wunder/init')
def authwInit():
 	code=request.args.get('code')

 	url = 'https://www.wunderlist.com/oauth/access_token'
 	payload = {'client_id':'541ab1f4caa4896bb47d','client_secret':'9c3fad36181643f1cbc80d8ef3d3dbaa57fe279bb1e6c7b03021d81d99f2','code':code}
 	headers = {'content-type':'application/json'}
 	wunderAccessToken = ast.literal_eval(requests.post(url,data=json.dumps(payload),headers=headers).content)['access_token']

	return redirect("ToDoAuthInit://?type=wunderlist&token="+wunderAccessToken, code=302)

if __name__ == "__main__":
	application.run(host="0.0.0.0")
