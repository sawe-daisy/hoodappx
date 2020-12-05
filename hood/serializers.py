from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from .models import Neighborhood, Profile, Post



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff','password']

        def create(self, validated_data):
            validated_data['password']= make_password(validated_data.get('password'))
            return super(UserSerializer, self).create(validated_data)

class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    email=serializers.EmailField()
    fName=serializers.CharField(required=False)
    lName=serializers.CharField(required=False)
    password=serializers.CharField()
    confPass=serializers.CharField()

    def validateEmail(self, email):
        existing=User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError('Email taken')
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confPass'):
            raise serializers.ValidationError('Enter a password and confirm it')
        if data.get('password') != data.get('confPass'):
            raise serializers.ValidationError("'The passwords don't match")

class HoodSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Neighborhood
        fields = ['name', 'location', 'count'] 

class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Neighborhood
        fields = '__all__' 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields=['description', 'post_image', 'categories']

class ProfileSerializer(serializers.ModelSerializer):
    neighbourhood = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['profile_pic', 'idNo', 'neighbourhood', 'status', 'user'] 

