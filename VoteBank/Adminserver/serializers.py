from rest_framework import serializers
from Adminserver.models import Candidates, Voter

class Voterserializers(serializers.ModelSerializer):
    class Meta:
        model=Voter
        fields=['id','name','constituency','state','hasvoted']

class Candidateserilizer(serializers.ModelSerializer):
    class Meta:
        model=Candidates
        fields=['id','name','party','code','e','n']

class SecreatsCandidateserilizer(serializers.ModelSerializer):
    class Meta:
        model=Candidates
        fields=['id','name','party','code','e','n','d']