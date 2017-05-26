import os
from flask import Flask, redirect, render_template

application = Flask(__name__)

@application.route('/')
def home():
	return render_template('index.html')
@application.route('/auth')
def auth():
	return redirect("ToDoAuth://",code=302)


if __name__ == "__main__":
    application.run(host="0.0.0.0")
