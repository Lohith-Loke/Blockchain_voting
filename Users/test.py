import json,requests
# dk=json.load(open("./.block.json","r"))
dk=json.load(open("./.fake/block.json","r"))

r=requests.post("http://127.0.0.1:8080/blocks/",json=dk)
resp=r.json()
if not resp or "error" in resp:
    print("error:",resp['error'])
print(resp)