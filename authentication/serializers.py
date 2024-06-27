from rest_framework import serializers
from .models import User, Candidate,Event,Application,Recruiter,Post,Message,UserStatus,Clients


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

from rest_framework import serializers
from .models import Candidate, Event

class CandidateSerializer(serializers.ModelSerializer):
     class Meta:
         model = Candidate
         fields = '__all__'


class RecruiterSerializer(serializers.ModelSerializer):
     class Meta:
         model = Recruiter
         fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    candidate = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all())

    class Meta:
        model = Application
        fields = ['candidate', 'post', 'status', 'additional_documents']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__' 

class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'