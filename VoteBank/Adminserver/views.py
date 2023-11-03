from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from Adminserver.models import Candidates, Signature,Voter
from Adminserver.serializers import Candidateserilizer, Voterserializers,SecreatsCandidateserilizer
from rest_framework.parsers import JSONParser

from Adminserver.crypt.publick_key import global_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


@api_view(['GET'])
def all_list(request):
    voters=Voter.objects.all()
    serialzed=Voterserializers(voters,many=True)
    return Response(serialzed.data)

@api_view(['GET','Post'])
@parser_classes([JSONParser])
def getvotes(request):
    if set(request.data.keys())!={'name','start','end','token','sign','hash','messege'}:
        return Response({"error":"missing params","errorcode":1})
    try:
        # verify hash of messsege 
        name=str(request.data['name'])
        start=str(request.data['start'])
        end=str(request.data['end'])
        rand=str(request.data['token'])
        hash_=str(request.data['hash'])
        sign=str(request.data['sign'])
        try :
            Signature.objects.get(pk=sign)
            # return Response({"error":"ballet recived already"})
            pass
        except Signature.DoesNotExist:
            # new signature 
            pass
        string= name+start+end+rand
        digest=hashes.Hash(hashes.SHA3_256())
        digest.update(bytes(string+sign,encoding="utf-8"))
        h=digest.finalize().hex()

        if hash_ != h:
            print(hash_)
            print(h)
            return Response({"error":"hash signatue","errorcode":100})
        
        print("hash verification sucessful")
        try:
            global_key.auth_pub.verify(
                signature=bytes.fromhex(sign),
                data=bytes(string,encoding="utf-8"),
                padding=padding.PKCS1v15(),
                algorithm=hashes.SHA3_256()
            )
            print("signature verifyed")
            signed_m_1=global_key.pk.sign(int(request.data["messege"]))
            p=Signature(sign=sign,m_blind=int(request.data["messege"]))
            # p.save()
            
            return Response({"params":"verified","bank_signature":signed_m_1})

        except InvalidSignature:
            print("signature miss match")
            return Response({"error":"signature varification failed","errorcode":12})
        
    except Exception as ex:
        print(f"exception{ex}")
        return Response({"error":"request validation failed ","errorcode":2})

@api_view(['GET'])
def get_keys(request):
    e,n=global_key.pk.get_pub()
    return Response({"e":e,"n":n})

@api_view(['GET'])
def get_candidates(request):
    candidates=Candidates.objects.all()
    serialzed=Candidateserilizer(candidates,many=True)
    return Response(serialzed.data)

@api_view(['GET'])
def secreats(request):
    candidates=Candidates.objects.all()
    serialzed=SecreatsCandidateserilizer(candidates,many=True)
    return Response(serialzed.data)