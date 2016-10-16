#!/usr/bin/env python
import json
import requests
import web

web.config.debug = False

urls = (
    "/login", "login",
    "/logout", "logout",
    "/fcLogin", "fcLogin",
    "/getUser", "getUser"
)

config_file = "config.json"
private_file = "private.json"

authorization_url= ""
token_url = ""
userinfo_url = ""
logout_url = ""

clef = ""
secret = ""

clientId = "18712345678912345"

request_uri = ""
scope= ""

with open(config_file) as json_file:
    json_data = json.load(json_file)
    authorization_url = json_data["authorization_url"]
    token_url = json_data["token_url"]
    userinfo_url = json_data["userinfo_url"]
    logout_url = json_data["logout_url"]
    request_uri = json_data["request_uri"]
    scope= json_data["scope"]

with open(private_file) as json_file:
    json_data = json.load(json_file)
    clef = json_data["clef"]
    secret = json_data["secret"]

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': "null"})

def get_fc_authorize(client_id, redirect_uri, state, nonce):
    url = authorization_url + "?response_type=code&client_id=" + client_id + "&redirect_uri=" + request_uri + "&scope=" + scope + "&state=" + state + "&nonce=" + nonce + " Authorize"
   
    res = '{ "url": "' + url + '" }'
    print(res)
    return res

def post_fc_token(code, redirect_uri, client_id, client_secret):
    url = token_url
    data={
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }
   
    res = requests.post(url, data=data)
    print(res.text)
    return json.loads(res.text)
   
def get_fc_userinfo(access_token):
    url = userinfo_url
    headers = {
       "Authorization": "Bearer " + access_token
    }
    res = requests.get(url, headers=headers)
    session.user = res.text
    print(session.user)
    return res.text

def get_fc_logout():
    url = logout_url
    res = requests.get(url)
    
    print(res.text)
    
    return res

class fcLogin:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')        
        json_res = get_fc_authorize(clef, request_uri, "test", "test")
        return json_res

class login:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        
        code = web.input().code

        json_res = post_fc_token(code, request_uri, clef, secret)
        access_token = json_res["access_token"]
        return get_fc_userinfo(access_token) 
        
class logout:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        get_fc_logout()
        return '{"logged" : false}'

class getUser:
    def GET(self):
        web.header('Access-Control-Allow-Origin',      '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        return str(session.user)

if __name__ == "__main__":
    app.run()

