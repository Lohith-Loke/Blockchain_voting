from django.db import models

class Votes(models.Model):
    vote=models.CharField(max_length=2048)
    salt=models.CharField(max_length=500)
    sign=models.CharField(max_length=2048)

class Block(models.Model):
    top_hash=models.CharField(max_length=1024)
    vote=models.CharField(max_length=2048,primary_key=True)
    slat=models.CharField(max_length=500)
    time_stamp=models.DateTimeField()
    bottom_hash=models.CharField(max_length=1024)
