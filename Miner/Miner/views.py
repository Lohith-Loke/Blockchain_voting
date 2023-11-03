from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import JSONParser

from Miner.models import Votes
from Miner.serializers import Voteserilizer

@api_view(['GET'])
def all_votes(request):
    vote=Votes.objects.all()
    serialized=Voteserilizer(vote,many=True)
    return Response(serialized.data)

@api_view(['GET','POST'])
@parser_classes([JSONParser])
def verify_vote(request):
    if ({'vote','salt'}-set(request.data.keys()))=={}:
        return Response({"error":"missing params","errorcode":1})
    
    v=Votes(
        vote=str(request.data['vote']),
        salt=str( request.data['salt']),
        sign = str(request.data['sign']) 
    )
    v.save()
    return Response({"vote_status":"accepted"})
