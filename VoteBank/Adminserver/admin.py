from django.contrib import admin
from .models import Candidates, Signature, Voter

admin.site.register(Voter)
admin.site.register(Candidates)
admin.site.register(Signature)