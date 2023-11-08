from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser
from Miner.models import Block
from Miner.serializers import Blockserilizers
# from Miner.init.genesisblock import Genesis_Block
from Miner.models import Votes
from Miner.serializers import Voteserilizer
import requests

@api_view(['GET'])
def all_votes(request):
    vote=Votes.objects.all()
    serialized=Voteserilizer(vote,many=True)
    return Response(serialized.data)

@api_view(['GET','POST'])
@parser_classes([JSONParser])
def verify_vote(request):
    # print({'vote','salt','sign'}-set(request.data.keys())=={})
    if ({'vote','salt','sign'}-set(request.data.keys()))!={}:
        return Response({"error":"missing params","errorcode":1})
    v=Votes(
        vote=str(request.data['vote']),
        salt=str( request.data['salt']),
        sign = str(request.data['sign']) 
    )
    try:
        v.save()
        return Response({"vote_status":"accepted"})
    except:
        return Response({"vote_status":"Falied",'error':'vote already accepted'})


@api_view(['GET'])
def get_blocks(request):
    # if Genesis_Block.top_hash=="genesis":
        # pass
    blocks=Block.objects.all()
    serialized=Blockserilizers(blocks,many=True)
    return Response(serialized.data)

@api_view(['GET','POST'])
@parser_classes([JSONParser])
def post_blocks(request):
    if {'vote','salt','tophash','sign','timestamp','nonce','bottomhash'}-set(request.data.keys())=={}:
        return Response({"error":"missing params","errorcode":1})
    print(' correct params')
    print(request.data)
    def verifyvote(vote:int,sign:int):
        r=requests.get("http://127.0.0.1:8888/keys/")
        resp=r.json()
        if not resp or "error" in resp:
            print("unbale to conect to Votebank server ")
            return 
        bank=r.json()
        bank["e"]=int(bank['e'])
        bank["n"]=int(bank['n'])
        if (vote)==(pow(sign,bank["e"] , bank["n"])%bank["n"]):
            return True
        else:
            return False
    if not verifyvote(int(request.data['vote']),int(request.data['sign'])):
        return  Response({"Block_status ":"failed ","error":"unable to veify votes "})
    block=Block(
        top_hash=str(request.data['tophash']),
        vote=str(request.data['vote']),
        salt=str( request.data['salt']),
        sign = str(request.data['sign']),
        time_stamp=str(request.data['timestamp']),
        nonce=str(request.data['nonce']),
        bottom_hash=str(request.data['bottomhash'])
    )
    print('Block object created ')
    block.save()
    return Response({"Block_status ":"accepted"})