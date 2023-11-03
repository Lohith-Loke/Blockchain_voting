from rest_framework import serializers
from polls.models import AdharCard


class AdharCardsserializers(serializers.ModelSerializer):
    class Meta:
        model=AdharCard
        fields=["name","adharnumber","phone_number"]

# class Signatureserializers(serializers.ModelSerializer):
#     class Meta:
#         # {"name":e_name,"start":e_start, "end":e_end, "data":rand,"sign":sign}

#         fields=["name","start","end","data","sign","hash"]