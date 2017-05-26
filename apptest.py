#!/usr/bin/env python
import bottle
from bottle import route, run, default_app, static_file, request, response, template, SimpleTemplate
import requests
import json
import ast
import os.path
import arrow
import os

# test
# open('/var/www/wunderCan/logging.txt','w').write('test')
dir_path = os.path.dirname(os.path.realpath(__file__))

def website():
    web = open('website.txt','w')
    web.write('is website run? yes')
    web.close()

    app = bottle.Bottle()

    #bottle.TEMPLATE_PATH.insert(0, 'views')

    @app.route('/')
    def home_page():
    	#cookies_log = open("cookies.txt","a")
    	if request.get_cookie("bigUId"):
    		#cookies_log.write("cookie found")
    	        resp = template("index")
    		#response.set_cookie("bigUId", "uid12345")
    		#ookies_log.close()
    		return resp
    	else:
    		resp = template("index")
    		#response.set_cookie("bigUId", "uid12345")
    		#cookies_log.write("No cookie found. Adding one")
    		#cookies_log.close()
    		return resp

    @app.route('/hellow')
    def test():
    	aCookie = request.get_cookie('wunderToken')
       	aResponse = bottle.template('Hello, it is {{val}}', val=aCookie)
    	return aResponse

    @app.route('/static/<filepath:path>')
    def static(filepath):
    	return static_file(filepath, root='./static')

    @app.route('/views/<filepath:path>')
    def view_static(filepath):
    	return static_file(filepath, root='./views')

    @app.route('/authorize/wunder')
    def authorizeWunder():
        # get parameters
        state = request.query.state
        code = request.query.code

        # exchange code for access token
        url = 'https://www.wunderlist.com/oauth/access_token'
        payload = {'client_id':'541ab1f4caa4896bb47d','client_secret':'9c3fad36181643f1cbc80d8ef3d3dbaa57fe279bb1e6c7b03021d81d99f2','code':code}
        headers = {'content-type':'application/json'}
        wunderAccessToken = ast.literal_eval(requests.post(url,data=json.dumps(payload),headers=headers).content)['access_token']

        resp = template("index")

        # set as cookie
        response.set_cookie('wunderToken',wunderAccessToken, path='/')

        # redirect to 0.0.0.0:8081#one
        return resp

    @app.route('/authorize/canvas')
    def authorizeCanvas():
      # get parameters
        state = request.query.state
        code = request.query.code
    
        # exchange code for access token
        url = 'https://nuevaschool.instructure.com/login/oauth2/token'
        payload = {'grant_type':'authorization_code','client_id':'52960000000000002','client_secret':'I5TXjoH4cG2bUbDuYYEKloVguAftsTpXE4aILIZIxVXKXenZHGlF4GG3rdhyVcre','redirect_uri':'http://wundercan.tk/authorize/canvas','code':code}
        headers = {'content-type':'application/json'}
        canvasAccessToken = ast.literal_eval(requests.post(url,data=json.dumps(payload),headers=headers).content)['access_token']
    
        resp = template("index")
        # set as cookie
        response.set_cookie('canvasToken',canvasAccessToken, path='/')    
    
        #TODO
        # store canvas access token in canvasToken cookie
        return resp

    @app.route('/download')
    def download():
        wunderAccessToken = request.get_cookie('wunderToken')
        canvasAccessToken = request.get_cookie('canvasToken')

        # TODO: set access tokens in scraper to the above tokens

        # testing forced download. replace this with downloaded file
        return static_file('index.html', root='./views', download=True)

    return app
    



class StripPathMiddleware(object):
    '''
        Get that slash out of the request
        '''
    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)


if __name__ == '__main__':
    bottle.run(app=StripPathMiddleware(website()),
               host='0.0.0.0',
               port=8081)
if __name__.startswith('app'):
    #uwsgi = open("/var/www/wunderCan/uwsgiTest.txt","w")
    #uwsgi.write("uwsgi success")
    #uwsgi.close()
    #paths = open("/var/www/wunderCan/paths.txt","w")
#    paths.write("Default Directory:"+os.getcwd())
 #   paths.write("os.path.dirname(__file__) is"+os.path.dirname(__file__))
  #  paths.write("os.path.dirname(os.path.realpath(__file__)) is "+os.path.dirname(os.path.realpath(__file__)))
   # paths.write("os.path.realpath(__file__) is "+os.path.realpath(__file__))
    #paths.close()
    os.chdir(os.path.dirname(__file__))
    app = application = website()

