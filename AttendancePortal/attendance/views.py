from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import AttendanceSerializer, LectureSerializer, BatchSerializer
from .models import Attendance, Batch, Lecture
from accounts.models import *
import csv 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.custompermision import IsTeacher
# Create your views here.

#----------------Lecture Views Here-------------------------
class LectureAPI(GenericAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    def post(self, request):
        lecture = LectureSerializer(data = request.data)
        if not lecture.is_valid():
            return Response(data= {'error':lecture.errors}, status=status.HTTP_400_BAD_REQUEST)
        lecture.save()
        return Response(data = {'lecture_id': lecture.data['id']}, status=status.HTTP_201_CREATED)

#----------------Batch Views Here -------------------------

class BatchAPI(GenericAPIView):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
    def post(self, request):
        data_dict={}
        for key in request.data:
            data_dict[key] =  request.data[key]
        data_dict['students'] = data_dict.get('students','[]').strip('][}{)(').split(',')
        batch = BatchSerializer(data=data_dict)
        if not batch.is_valid():
            return Response(data= {'error':batch.errors}, status=status.HTTP_400_BAD_REQUEST)
        batch.save()
        return Response(data = {'batch_id': batch.data['id']}, status=status.HTTP_201_CREATED)
    
#-------------Attendance Views---------------------------

class AttendanceAPI(GenericAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    def post(self,request):
        instance = request.data
        for i in instance:
            try:
                instance1 = Attendance.objects.get(lecture = i['lecture'], student = i['student'])
                serializer = AttendanceSerializer(instance1,data = i)
                if serializer.is_valid():
                    serializer.save()
            except ObjectDoesNotExist:
                serializer = AttendanceSerializer(data = i)
                if serializer.is_valid():
                    serializer.save()
        lecture = Lecture.objects.get(id = instance[0]['lecture'])
        lecture.attendance_taken = True
        lecture.save()    
        return Response(data = {"message":"Attendance created successfully"} ,status=status.HTTP_201_CREATED)

    def patch(self, request):
        try:
            instance = Attendance.objects.get(lecture = request.data['lecture'], student = request.data['student'])
            serializer = AttendanceSerializer(instance,data = request.data)
            if serializer.is_valid():
                serializer.save()
        except ObjectDoesNotExist:
            serializer = AttendanceSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
        return Response(data = {"message":"Student attendance updated successfully"} ,status=status.HTTP_202_ACCEPTED)
        
#-------------Download Attendance Views---------------------------

class DownloadAttendanceAPI(GenericAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    def post(self,request):
        try:
            lecture = request.data['lecture']
            lecture_obj = Lecture.objects.get(id = lecture)
            attendance = Attendance.objects.filter(lecture = lecture)
            attendance_list = [{"Sap id":i.student.user.sap_id,"Name":i.student.user.getfullname() ,"Present":i.present} for i in attendance]
            fields = ["Sap id", "Name", "Present"] 
            filename = f"attendancefiles/{lecture_obj.batch.define()}_{lecture_obj.subject.name}_startTime({lecture_obj.startTime.hour}-{lecture_obj.startTime.minute})_endTime({lecture_obj.endTime.hour}-{lecture_obj.endTime.minute})_date({lecture_obj.date}).csv"
            with open(filename, 'w') as csvfile: 
                writer = csv.DictWriter(csvfile, fieldnames = fields) 
                writer.writeheader() 
                writer.writerows(attendance_list)
            with open(filename) as csvfile:
                response = HttpResponse(csvfile, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
                return response
        except KeyError:
            return Response(data= {'error':{"lecture":["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data= {'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
#-------------Assigned Teacher Lecture Views---------------------------
class AssignedTeacherLectureAPI(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get(self, request):
        serializer = LectureSerializer(Lecture.objects.filter(teacher = Teacher.objects.get(user = request.user.id).id), many = True)
        serialized_data = {}
        serialized_data['Lectures'] = [{
            'id' : i['id'], 
            'startTime': i['startTime'],
            'startTime': i['startTime'],
            'endTime': i['endTime'],
            'date': i['date'],
            'note': i['note'],
            'attendance_taken': i['attendance_taken'],
            'batch' : {
                'id' : i['batch']['id'],
                'semester': i['batch']['semester'],
                'year': i['batch']['year'],
                'name': i['batch']['name'],
                'number_of_students': i['batch']['number_of_students'],
            },
            'subject':{
                'id' : i['subject']['id'],
                'name' : i['subject']['name']
            }}
            for i in serializer.data]
        return Response(serialized_data)