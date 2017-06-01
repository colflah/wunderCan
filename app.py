
#!/usr/bin/env python
import bottle
from bottle import route, run, default_app, static_file, request, response, template, SimpleTemplate
import requests
import json
import ast
import os.path
import arrow

# test
# open('/var/www/wunderCan/logging.txt','w').write('test')

app = application = bottle.Bottle()

@app.route('/')
def home_page():
	return static_file('index.html', root='/var/www/wunderCan')

@app.route('/hellow')
def test():
	aCookie = request.get_cookie('wunderToken')
	aResponse = SimpleTemplate('Hello, it is {{aCookie}}}')	
	try:
#		return aResponse
		return static_file('index2.html', root='/var/www/wunderCan')
	except Exception as e:
		log = ["Date: "+arrow.utcnow().to('US/Pacific'),"Request: /hellow", "Exception: "+e]
		if os.path.isfile('/var/www/wunderCan/exceptions.txt'):
			open('/var/www/wunderCan/exceptions.txt','a').writelines(log).close()
		else:
			open('/var/www/wunderCan/exceptions.txt','w').writelines(log).close()
		return static_file('index2.html',root='/var/www/wunderCan')

@app.route('/static/<filepath:path>')
def static(filepath):
	return static_file(filepath, root='/var/www/wunderCan/static')

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

    # set as cookie
    response.set_cookie('wunderToken',wunderAccessToken, path='/')

    # redirect to 0.0.0.0:8081#one
    return wunderAccessToken


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
    
    # set as cookie
    response.set_cookie('canvasToken',canvasAccessToken, path='/')    
    
    #TODO
    # store canvas access token in canvasToken cookie
    return canvasAccessToken

@app.route('/download')
def download():
    wunderAccessToken = request.get_cookie('wunderToken')
    canvasAccessToken = request.get_cookie('canvasToken')

    # TODO: set access tokens in scraper to the above tokens

    # testing forced download. replace this with downloaded file
    # return static_file('index.html', root='/var/www/wunderCan',download='example.html')
    return "TODO"


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
    bottle.run(app=StripPathMiddleware(app),
               host='0.0.0.0',
               port=8081)

