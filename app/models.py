from django.db import models

# Create your models here.
class orderdata(models.Model):
    blood=models.CharField(max_length=3)
    quantity=models.FloatField()
    by=models.CharField(max_length=200)
    address=models.CharField(max_length=300)
    orderdate=models.DateField()
    shipdate = models.DateField()
    phone=models.IntegerField()
    def __str__(self):
        return self.by

class donor(models.Model):
    first=models.CharField(max_length=50)
    last = models.CharField(max_length=50)
    email=models.CharField(max_length=40,primary_key=True)
    phone=models.IntegerField(unique=True)
    gender=models.CharField(max_length=6)
    dob=models.DateField()
    country=models.CharField(max_length=20)
    state= models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    aadhar=models.IntegerField(unique=True)
    blood=models.CharField(max_length=3)
    quantity=models.FloatField()
    def __str__(self):
        return self.email
class bloodtype(models.Model):
    blood=models.CharField(max_length=3,primary_key=True)
    quant=models.FloatField()
    cost=models.IntegerField()
    def __str__(self):
        return self.blood

class yadmin(models.Model) :
    first = models.CharField(max_length=50)
    last=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    passw=models.CharField(max_length=100)
    def __str__(self):
        return self.username
