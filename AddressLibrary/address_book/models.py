from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Persons(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('first_name','last_name',)


class Groups(models.Model):
    name = models.CharField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('name',)


class Members(models.Model):
    person = models.ForeignKey(Persons)
    group = models.ForeignKey(Groups)
    created = models.DateTimeField(auto_now_add=True,)


class Street_Addresses(models.Model):
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('country','state','city',)
        unique_together = ('country', 'state', 'city')


class Person_Street_Addresses(models.Model):
    person = models.ForeignKey(Persons)
    street_address = models.ForeignKey(Street_Addresses)
    area = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class Person_Email_Addresses(models.Model):
    person = models.ForeignKey(Persons)
    email = models.EmailField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class Person_Phone_Numbers(models.Model):
    person = models.ForeignKey(Persons)
    country_code = models.CharField(max_length=5)
    phone_no = models.CharField(max_length=15)

    class Meta:
        unique_together = ('country_code', 'phone_no')