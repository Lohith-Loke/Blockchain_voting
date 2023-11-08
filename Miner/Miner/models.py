import hashlib
from django.core.exceptions import ValidationError

from django.db import models


class Votes(models.Model):
    vote=models.CharField(max_length=2048,primary_key=True)
    salt=models.CharField(max_length=500)
    sign=models.CharField(max_length=2048)

class Block(models.Model):
    top_hash=models.CharField(max_length=1024)
    vote=models.CharField(max_length=2048,unique=True)
    salt=models.CharField(max_length=500)
    sign=models.CharField(max_length=2048)
    time_stamp=models.CharField(max_length=12)
    nonce=models.CharField(max_length=50)
    bottom_hash=models.CharField(max_length=1024,primary_key=True)
    counter=models.BigIntegerField(auto_created=True,editable=False,default=1)
    def save(self,*args,**kwargs):
        try:
            if len(Block.objects.all())==0:
                return super(Block,self).save(*args,**kwargs)
            # verify the vote
            
            last_block=Block.objects.get(bottom_hash=self.top_hash)
            #check for vote repetation 
            pre_block=last_block
            
            while True:
                if pre_block.top_hash=='genesis':
                    break # reached genesis
                if self.vote!=pre_block.vote:
                    pre_block=Block.objects.get(pk=pre_block.top_hash)
                else:
                    print(" duplicate vote in chain")
                    raise ValidationError(" duplicate vote in chain")
            # blockchain verified block's legitimasy 
            input_string=f'{self.top_hash}{self.vote}{self.salt}{self.time_stamp}{self.nonce}'
            hash_hex = hashlib.sha3_256(input_string.encode()).hexdigest()
            if hash_hex!=self.bottom_hash:
                print("Hash missmach")
                ValidationError("Hash missmach")
            self.counter=last_block.counter+1
        except Block.DoesNotExist:
            print("could not find previous block ")
            raise ValidationError(" could not find previous block ")
        super(Block,self).save(*args,**kwargs)
