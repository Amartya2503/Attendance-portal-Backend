from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.generics import GenericAPIView

# Create your views here.
class hello(GenericAPIView):

    def get(sel,request):

        return Response("hello world from this app ")

 