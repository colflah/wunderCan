import os
from flask import Flask, redirect, render_template, request
import ast
import requests
import json

application = Flask(__name__)

@application.route('/')
def home():
	return render_template('index.html')

@application.route('/auth/Todoist')
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


if __name__ == "__main__":
    application.run(host="0.0.0.0")
