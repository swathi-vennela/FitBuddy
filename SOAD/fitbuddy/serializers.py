from rest_framework import serializers
from .models import Program, Review, HiringRole

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    program_name = serializers.CharField(source='program.title')
    class Meta:
        model = Review
        fields=('id','program_name','username','comment','rating')

class ProgramSerializer(serializers.ModelSerializer):
    fitnesscenter_name = serializers.CharField(source='fcenter.fitnesscenter_name')
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Program
        fields=('id','title','category','number_of_sessions','hours_per_session','price','description','image','fitnesscenter_name','reviews')

class HiringRoleSerializer(serializers.ModelSerializer):
    fprogram_name = serializers.CharField(source='fprogram.title')
    class Meta:
        model = HiringRole
        fields=('fprogram_name','role','title','salary','qualifications','responsibilities','gender','contact_email','slug')

