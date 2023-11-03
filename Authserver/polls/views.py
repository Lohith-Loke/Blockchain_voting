from rest_framework.response import Response
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from rest_framework.decorators import api_view,parser_classes
from polls.models import AdharCard,Election
from polls.serializers import AdharCardsserializers
from rest_framework.parsers import JSONParser
from .keys import global_key


@api_view(['GET'])
def all_list(request):
    adhar=AdharCard.objects.all()
    serialized=AdharCardsserializers(adhar,many=True)
    return Response(serialized.data)

@api_view(['GET','POST'])
@parser_classes([JSONParser])
def genarte(request):
    # required keys
    # name,adhar number,dob,

    if ({"name","adhar_number","dob","phone_number"}-set(request.data.keys()))=={}:
        return Response({"error":"missing params","errorcode":1,"missing":set(request.data.keys())})
    try:
        adhar=AdharCard.objects.get(pk=request.data["adhar_number"])
        if (adhar.name==request.data["name"]) and (adhar.phone_number==request.data["phone_number"]) and (str(adhar.dob)==request.data["dob"]):
            print("Auth sucessfull")
            election=Election.objects.get(id=1)
            rand=adhar.rand
            name=str(election.name)
            start=str(election.start_date)
            end=str(election.End_date)
            string=name+start+end+rand

            # print(string)
            sign=global_key.pk.sign(
                data=bytes(string,encoding="utf-8"),
                algorithm=hashes.SHA3_256(),
                padding=padding.PKCS1v15()
            )
            dk={"name":name,"start":start, "end":end, "token":rand,"sign":sign.hex()}
            digest=hashes.Hash(hashes.SHA3_256())
            digest.update(bytes(string+sign.hex(),encoding="utf-8"))
            dk["hash"]=digest.finalize().hex()
            return Response(data=dk)

        serialized=AdharCardsserializers(adhar,many=False)
        return Response(serialized.data)

    except AdharCard.DoesNotExist:
        return Response({"error":"record not found","errorcode":2})
    except Exception as e:
        return Response({"errror":"internal server error","e.type":e})

