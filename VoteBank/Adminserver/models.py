import hashlib
import os
from random import randint
from django.db import models
from Adminserver.crypt.publick_key import create_keys

class Voter(models.Model):
    name=models.CharField(max_length=200)
    constituency=models.CharField(max_length=20)
    state=models.CharField(max_length=15)
    hasvoted=models.BooleanField(auto_created=True,default=False,blank=True,editable=False)

    def __str__(self) -> str:
        return f'{self.name} {self.constituency}'

class Signature(models.Model):
    sign=models.CharField(max_length=1024,primary_key=True)
    m_blind=models.CharField(max_length=1024)

class Candidates(models.Model):
    name=models.CharField(max_length=12)
    party=models.CharField(max_length=20)
    code=models.IntegerField(auto_created=True,default=None,unique=True,editable=False)
    e=models.CharField(max_length=10000,auto_created=True,default=None,blank=True,editable=False)
    n=models.CharField(max_length=10000,auto_created=True,default=None,blank=True,editable=False,unique=True)
    d=models.CharField(max_length=10000,auto_created=True,default=None,blank=True,editable=False,unique=True)

    def save(self,*args,**kwargs) -> None:
        self.code=randint(pow(10,5),pow(10,12))
        self.e,self.n,self.d=create_keys(self.name)
        return super(Candidates,self).save(self,*args,**kwargs)
    def __str__(self)->str:
        return f'{self.name},{self.party}'
    