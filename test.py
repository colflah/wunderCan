import os
from flask import Flask, redirect, render_template, request
import ast
import requests
import json

#exchange code for access token, assign to token variable
code = '99601e57acabc0ec8389bb8e74a4c589aef35f7f'
url = 'https://www.todoist.com/oauth/access_token'
payload = {'client_id':'384c0e4c54944eb9ab951f345cbcff9f','client_secret':'30e67a1fdf464ac7aedb2cfa9b37c077','code':code}
headers = {'content-type':'application/json'}
token = requests.post(url,data=json.dumps(payload),headers=headers).content
#token = 'test'
print(token)

