import hashlib, requests, datetime,json

def verify(messege,sign,e_a,n_a):    
    if messege == (pow(sign, e_a, n_a))%n_a:
        return True
    else:
        return False
def MineBlocks(bank):
    def mine(input_string, target_zeros):
        nonce = 0
        target_prefix = "0" * target_zeros
        while True:
            data = input_string + str(nonce)
            hash_hex = hashlib.sha3_256(data.encode()).hexdigest()
            if hash_hex[:target_zeros] == target_prefix:
                return nonce, hash_hex
            nonce += 1
        
    while True:
        r=requests.get('http://127.0.0.1:8080/getblocks/')
        resp=r.json()
        if not resp or "error" in resp:
            print("unbale to conect to pool(miner) server ")
            return
        Blocks=resp

        r=requests.get('http://127.0.0.1:8080/getvotes/')
        resp=r.json()
        if not resp or "error" in resp:
            print("unbale to conect to pool(miner) server ")
            return
        All_votes=resp

        All_votes.reverse()
        Blocks.reverse()
        j=0
        isused=False

        for vote in All_votes:
            for  block in Blocks:
                if vote['vote']==block['vote']:
                    isused=True
                    break 
            if not isused and verify(int(vote['vote']),int(vote['sign']), bank['e'] , bank['n']):
                time=str(datetime.datetime.now())
                inputstr=f"{Blocks[0]['bottom_hash']}{vote['vote']}{vote['salt']}{time}"
                nonce,hash_hex=mine(inputstr,5)
                dk={
                'tophash':Blocks[0]['bottom_hash'],
                'vote':vote['vote'],
                'salt':vote['salt'],
                'sign':vote['sign'],
                'timestamp':time,
                'nonce':nonce,
                'bottomhash':hash_hex
                }
                json.dump(dk,open('.block.json','w'))
                r=requests.post('http://127.0.0.1:8080/blocks/',json=dk)
                resp=r.json()
                if not resp or "error" in resp:
                    print("error:",resp['error'])
                    print("unbale to conect to pool(miner) server ")
                    return
                



def main():
    r=requests.get("http://127.0.0.1:8888/keys/")
    resp=r.json()
    if not resp or "error" in resp:
        print("unbale to conect to Votebank server ")
        return 
    bank=r.json()
    bank["e"]=int(bank['e'])
    bank["n"]=int(bank['n'])
    r=requests.get('http://127.0.0.1:8080/getblocks/')
    resp=r.json()
    if not resp or "error" in resp:
        print("unbale to conect to pool(miner) server ")
        return 
    Blocks=resp
    r=requests.get('http://127.0.0.1:8080/getvotes/')
    resp=r.json()
    if not resp or "error" in resp:
        print("unbale to conect to pool(miner) server ")
        return 
    all_votes=resp
    if len(Blocks)>=len(all_votes):
        print("All votes are in block ")# mostly true 
        return
    MineBlocks(bank)

if __name__=="__main__":
    main()
            

    
