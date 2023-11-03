from rest_framework import serializers

from Miner.models import Votes

class Voteserilizer(serializers.ModelSerializer):
    class Meta:
        model=Votes
        fields=['vote','salt','sign']
    