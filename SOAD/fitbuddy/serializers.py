from rest_framework import serializers
from .models import Program, FitnessCenter

class ProgramSerializer(serializers.ModelSerializer):
    fitnesscenter_name = serializers.CharField(source='fcenter.fitnesscenter_name')
    class Meta:
        model = Program
        fields=('id','title','category','number_of_sessions','hours_per_session','price','description','image','fitnesscenter_name')

