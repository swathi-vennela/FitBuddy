from rest_framework import serializers
from .models import *
from datetime import datetime
from django.utils.text import slugify


class FitnessProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    directions_to_use = serializers.CharField()
    composition = serializers.CharField()
    price = serializers.FloatField()

    def create(self, validated_data):
        return FitnessProduct.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.directions_to_use = validated_data.get('directions_to_use', instance.directions_to_use)
        instance.composition = validated_data.get('composition', instance.composition)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


    class Meta:
        model = FitnessProduct
        fields = ("id","title","description","directions_to_use","composition","price","slug",)
