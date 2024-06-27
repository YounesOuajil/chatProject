from rest_framework import serializers
from authentication.models import Recruiter
class RecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = '__all__'
