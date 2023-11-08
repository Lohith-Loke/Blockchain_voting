from rest_framework import serializers

from Miner.models import Votes,Block

class Voteserilizer(serializers.ModelSerializer):
    class Meta:
        model=Votes
        fields=['vote','salt','sign']
class Blockserilizers(serializers.ModelSerializer):
    class Meta:
        model=Block
        fields=['top_hash','vote','salt','time_stamp','nonce','bottom_hash']
    