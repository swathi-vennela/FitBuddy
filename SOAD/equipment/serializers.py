from rest_framework import serializers
from .models import *
from datetime import datetime
from django.utils.text import slugify


class FitnessEquipmentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=50)
    description = serializers.CharField()
    price = serializers.FloatField()

    def create(self, validated_data):
        return FitnessEquipment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    class Meta:
        model = FitnessEquipment
        fields = ("id", "title", "type", "description", "price", "slug",)
