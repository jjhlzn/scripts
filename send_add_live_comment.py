import json
import urllib2

data = {
    "userInfo": {"token": "", "userid": ""}
}

req = urllib2.Request("http://localhost:1818/comment/addLive")
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))