import json
import requests
class helper():
    def verify(self,messege,sign,e_a,n_a):    
        if messege == (pow(sign, e_a, n_a))%n_a:
            return True
        else:
            return False
    def decript(self,cifer,d,e_a,n_a):
        # m = cd mod n
        return pow(cifer,d,n_a)%n_a
    def dataparcer(data):
        res=[]
        for i in data:
            dk={}
            dk['vote']=i['fields']['vote']
            dk['vote']=i['fields']['salt']
            dk['vote']=i['fields']['sign']
            res.append(dk)
        return res



        
def validate():
    r=requests.get("http://127.0.0.1:8888/keys/")
    resp_keys=r.json()
    h=helper()
    if resp_keys and "error" not in resp_keys:
       bank=r.json()
       bank["e"]=int(bank['e'])
       bank["n"]=int(bank['n'])
    else:
        # print("unable to get public keys")
        return 
    r=requests.get('http://127.0.0.1:8080/')
    resp=r.json()
    verified=[]
    if resp and "error" not in resp:
        for vote in resp:
            ToF=h.verify(int(vote['vote']),int(vote['sign']),bank['e'],bank['n'])
            if ToF:
               verified.append(vote)
            else:
                continue
    r=requests.get('http://127.0.0.1:8888/candidatekeys/')
    resp=r.json()

    if resp and "error" not in resp:
        candidates={}
        for key in resp:
            candidates[key['name']]=0
        for votes in verified:
            for idx,can in enumerate(candidates.keys()):
                m=h.decript(cifer=int(votes['vote']),d=int(resp[idx]['d']),e_a=int(resp[idx]['e']),n_a=int(resp[idx]['n']))
                ms=int(resp[idx]['code'])^int(votes['salt'])
                print(" m ^ salt ",ms)
                print("vote-decript  ",m)
                if m==ms:
                    candidates[can]+=1
        
        print(candidates)
validate()