from rest_framework import serializers
from models import *

class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'
        # read_only_fields = ('id',)


class PersonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persons
        fields = '__all__'
        # read_only_fields = ('id',)

class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class Street_AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street_Addresses
        fields = '__all__'

class Person_Street_AdressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person_Street_Addresses
        fields = '__all__'

class Person_Email_AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person_Email_Addresses
        fields = '__all__'

class Person_Phone_NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person_Phone_Numbers
        fields = '__all__'