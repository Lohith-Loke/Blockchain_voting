import math
import random
import requests
import json
import os
from sympy import mod_inverse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

class helper:
    @staticmethod
    def convet_tojson(data:dict)->dict:
        data
        dk={}
        dk["name"]=data["fields"]["name"]

        dk["adhar_number"]=data["pk"]
        dk["address"]=data["fields"]["address"]
        dk["phone_number"]=data["fields"]["phone_number"]
        dk["dob"]=data["fields"]["dob"]
        return dk
    
    @staticmethod
    def blind(m, pub_k):
        e_a, n_a = pub_k
        if m >= n_a:
            raise ValueError('Message must be smaller than n')
        while True:
            r = random.randint(2, n_a - 1)
            if math.gcd(r, n_a) == 1:
                break
        r_1 = mod_inverse(r, n_a)
        m_1 = (m * pow(r, e_a, n_a)) % n_a
        return m_1, r_1
    @staticmethod
    def encript(m,e,n):
        # C = m**e mod n
        return pow(m,e,n)
    
    @staticmethod
    def decript(cifer,d,e_a,n_a):
        # m = cd mod n
        return pow(cifer,d,n_a)%n_a

    @staticmethod
    def verify(m,sign,e,n):
        if m == (pow(sign, e, n))%n:
            return True
        else:
            return False    

def getsigns(idx:int):
    with open("./adhar.json") as fp:
        x=json.load(fp)
    if idx>len(x):
        print("voter not found")
        return
    voter_id=x[idx]
    voter_id=helper().convet_tojson(voter_id)
    r=requests.post("http://127.0.0.1:8000/post/",json=voter_id)
    return r.json()

def get_ballot(data:dict):
    # get bank keys 
    
    r=requests.get("http://127.0.0.1:8888/keys/")
    resp_keys=r.json()
    
    if resp_keys and "error" not in resp_keys:
       bank=r.json()
       bank["e"]=int(bank['e'])
       bank["n"]=int(bank['n'])
    else:
        print("unable to get public keys")
        return 
    
    list_of_candidates=requests.get("http://127.0.0.1:8888/candidatekeys/")
    print("code \t|| Candidate \t || party\t|| id ")
    for idx,option in enumerate(list_of_candidates.json()):
        print(f'{option["code"]}\t||{option["name"]}\t  || {option["party"]}\t|| {idx+1} ')

    vote=1 #or  int(input("pick id to vote :")) or 1
    lst_can=list_of_candidates.json()
    selected=list_of_candidates.json()[vote-1]
    
    print(f'voting to {selected["name"]}')

    salt=os.urandom(16)
    salt=int.from_bytes(salt, byteorder='big')
    
    messege = int(selected['code']) ^ salt
    
    
    e_c,n_c=int(selected['e']),int(selected['n']) 
    ms_c =helper().encript(messege,e_c,n_c)

    
    ms_c_1, r_1 = helper().blind(ms_c,(bank['e'],bank['n']))
    data["messege"]=ms_c_1
    
    r=requests.get("http://127.0.0.1:8888/vote/",json=data)
    resp=r.json()
    
    if resp and "error" not in resp:
        has_signed=helper().verify(m=ms_c_1,sign=resp['bank_signature'],e=bank['e'],n=bank['n'])
        print("bank siged on ms_c_1 ",has_signed)
        # sign_m = (r_1*sign_b_m_1)%bank_keys.n
        sign_ms_c=(r_1*int(resp['bank_signature'])%bank['n'])
        is_verified=helper().verify(ms_c,sign_ms_c,bank['e'],bank['n'])
        print( f'recovered sighn of bank on ms_c {is_verified}' )
        
        print("vote complete ")
        # resp['n']=bank['e']
        resp["signed_vote"]=sign_ms_c
        resp['salt']=salt
        resp["vote"]=ms_c
        data.update(resp)
        print(data)
        # json.dump(data,open("./.ballet.json","w"))
        votes={"vote":ms_c,"salt":salt,"sign":sign_ms_c}
        candidates={}
        for key in lst_can:
            candidates[key['name']]=0
        for idx,can in enumerate(candidates.keys()):
            ms=helper().decript(cifer=int(votes['vote']),d=int(lst_can[idx]['d']),e_a=int(lst_can[idx]['e']),n_a=int(lst_can[idx]['n']))
            ms_=int(lst_can[idx]['code']) ^ int(votes['salt'])
            print(ms)
            print(ms_)
            # if m==list_of_candidates[idx]['code']:
                # candidates[list_of_candidates[idx]['name']]+=1
                # break
        
        print(candidates)

        r=requests.post('http://127.0.0.1:8080/vote/',json={"vote":ms_c,"salt":salt,"sign":sign_ms_c}) 
        
        resp=r.json()
        if resp and "error" not in resp:
            print(resp)
            
        return True
    else:
        print(resp)

        return False

    
    # send m_hash to be signed by votebank server 
if __name__=="__main__":
    idx=3
    resp=getsigns(idx)
    print(resp)
    json.dump(resp,fp=open(file=".auth.json",mode="w",encoding="utf-8"))
    recived_ballot=get_ballot(json.load(open("./.auth.json")))
    if not recived_ballot:
        print("error in creating ballot")
