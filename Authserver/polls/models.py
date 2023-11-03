import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.conf import settings
class CustomValidators:
    @staticmethod
    def adharvalidator(value):
        if not value.isdigit() or len(value) != 12:
            raise ValidationError("The adhar number must be a 12-digit number.")
    @staticmethod
    def phonevalidator(value):
        if  not value.isdigit() or len(value)!=10:
            raise ValidationError("The phone number  must be a 10-digit number.")
    @staticmethod
    def dobvalidtor(value):
        if value > timezone.now().date():
            raise ValidationError("Date cannot be in the future ")
        # \\ to do set minimum year 
        if value<datetime.date(1930,1,1):
            raise ValidationError(f" date can't be older than {datetime.date(1930,1,1)} ")

class AdharCard(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    adharnumber = models.CharField(max_length=12, unique=True, validators=[CustomValidators.adharvalidator],primary_key=True)
    phone_number = models.CharField(max_length=10,validators=[CustomValidators.phonevalidator])  # You should define the appropriate max_length for phone numbers.
    dob=models.DateField(validators=[CustomValidators.dobvalidtor])
    rand=models.CharField(max_length=50,auto_created=True,default=get_random_string(length=20),editable=False)
    def __str__(self):
        return f"{self.name} {self.adharnumber}"
class Election(models.Model):
    name=models.CharField(max_length=30)
    level=models.IntegerField()
    start_date=models.DateTimeField()
    End_date=models.DateTimeField()
    Duration=models.DurationField(null=True,blank=True,editable=False)
    isused=models.BooleanField(default=False,blank=True,auto_created=True)
    def clean(self):
        # Call the parent class's clean method to run any default validation
        super(Election, self).clean()
        if self.start_date and self.End_date and self.start_date > self.End_date:
            raise ValidationError("Start date must be earlier than end date.")
    def save(self,*args,**kwargs):
        self.Duration=self.End_date-self.start_date
        super(Election,self).save(*args,**kwargs)
    
    def __str__(self) -> str:
        return self.name