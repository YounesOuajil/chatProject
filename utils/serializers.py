from rest_framework import serializers
from .models import Internship,Intern


class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'
class InternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intern
        fields = '__all__'
