from django.shortcuts import render
from .models import *
from .permissions import IsOwnerOrReadOnly
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


@api_view(http_method_names=['GET', 'POST', ])
@permission_classes([IsAuthenticated])
def fitnessequipment_list_view(request):
    if request.method == 'GET':
        return fitnessequipment_list_view_get(request)
    elif request.method == 'POST':
        return fitnessequipment_list_view_post(request)


@api_view(http_method_names=['GET', 'PUT', 'DELETE', ])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
def fitnessequipment_detail_view(request, slug):
    try:
        fequipment = Fitnessequipment.objects.get(title=slug)
        if request.method == 'GET':
            return fitnessequipment_detail_view_get(request, slug, fequipment)
        elif request.method == 'PUT':
            return fitnessequipment_detail_view_put(request, slug, fequipment)
        elif request.method == 'DELETE':
            return fitnessequipment_detail_view_delete(request, slug, fequipment)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def fitnessequipment_detail_view_get(request, slug, fequipment):
    serializer = FitnessequipmentSerializer(fequipment)
    return Response(serializer.data)


def fitnessequipment_detail_view_put(request, slug, fequipment):
    serializer = FitnessequipmentSerializer(fequipment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def fitnessequipment_detail_view_delete(request, slug, fequipment):
    delresult = fequipment.delete()
    data = {'message': 'error during deletion'}
    if delresult[0] == 1:
        data = {'message': 'successfully deleted'}
    return Response(data)


def fitnessequipment_list_view_get(request):
    try:
        data = Fitnessequipment.objects.all()
        serializer = FitnessequipmentSerializer(data, many=True)
        return Response(data=serializer.data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def fitnessequipment_list_view_post(request):
    if request.method == 'POST':
        serializer = FitnessequipmentSerializer(data=request.data)
        print("to be validated")
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        else:
            print("not valid")
            return Response(status=status.HTTP_400_BAD_REQUEST)

