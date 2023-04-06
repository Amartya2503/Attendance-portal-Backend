from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from .serializers import AttendanceSerializer, LectureSerializer, BatchSerializer
from .models import Attendance, Batch, Lecture

# Create your views here.
class LectureAPI(GenericAPIView, CreateModelMixin):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    def post(self, request):
        return self.create(request)
    # def get(self, request):
    #     pass

class CreateAttendance(GenericAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    def post(self,request):
        serializer = AttendanceSerializer(request.data,many = True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class AcessAttendance(GenericAPIView):
    serializer_class = AttendanceSerializer
    
    def get_object(self,pk):
        try:
            instance = Attendance.objects.get(sap_id = pk)
            return instance
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def get(self,request,pk):
        instance = object(pk)
        
        #this is incomplete 


