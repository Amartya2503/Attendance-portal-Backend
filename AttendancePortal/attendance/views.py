
from .dump import SAPDump,CustomSapDump
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.generics import GenericAPIView
from rest_framework import status
from .serializers import AttendanceSerializer, LectureSerializer, BatchSerializer, TeacherBatchSerializer, newBatchSerializer
from .models import Attendance, Batch, Lecture, TeacherBatch
from accounts.models import *
import csv 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.custompermision import IsTeacher
from django.conf import settings
from django.core.mail import send_mail
import datetime
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
        return Response(data = {'lecture_id': lecture.data['id']}, status=status.HTTP_200_OK)
    
    # serializer_class = LectureSerializer
    # queryset = Lecture.objects.all()

#-------------------Lecture patch and delete views---------------------

class EDLectureAPI(GenericAPIView):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()

    def get(self,request,id):
        try:
            l = Lecture.objects.get(id = id)
            serializer = LectureSerializer(l)
            return Response(data = {'data' : serializer.data},status= status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message' : f'Lecture with id {id} does not exist'},status= status.HTTP_404_NOT_FOUND)
        
    def patch(self,request,id):
        lec_id = id
        try:
            instance = Lecture.objects.get(id = lec_id)
            serializer = LectureSerializer(instance, data = request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                print("error",serializer.errors)
            return Response(data = {'message': f'updating {instance} with {request.data}','data': serializer.data},status = status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            print('nope')
            return Response(data ={'message': f'could not edit {instance}'},status = status.HTTP_400_BAD_REQUEST)
                    
    def delete(self,request,id):
        lec_id = id
        try:
            l =Lecture.objects.get(id = lec_id)
            print(l)
            l.delete()
            return Response(data = {'message': f'deleted {lec_id}'},status = status.HTTP_302_FOUND)
        except ObjectDoesNotExist:
            return Response(data = {'error':'Lecture DNE'},status = status.HTTP_404_NOT_FOUND)


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
    def delete(self,request):
        lec = Lecture.objects.get(id = request.data['id'])
        lec.delete()
    
#-------------Attendance Views---------------------------

class AttendanceAPI(GenericAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    def get(self,request):
        lec_id = request.data['lecture']
        if lec_id:
            serializer = AttendanceSerializer(Attendance.objects.filter(lecture = request.data['lecture']),many = True)
            serialized_data = {}
            serialized_data['Attendences'] = [{
                "id" : i['id'], 
                "date_time":i["date_time"],
                "present":i["present"],
                "lecture":{
                    "id":i["lecture"]["id"],
                    "teacher":{
                        "id":i["lecture"]["teacher"]["id"]
                    },
                    "batch":{
                        i["lecture"]["batch"]["id"]
                    }
                },
                "student":{
                    "id": i["student"]["id"],
                    "user":{
                        "id":i["student"]["user"]["id"],
                        "sap_id":i["student"]["user"]["sap_id"],
                        "first_name":i["student"]["user"]["first_name"],
                        "last_name":i["student"]["user"]["middle_name"],

                    }
                }
            }for i in serializer.data]

            return Response( serialized_data)
        else:
            return Response(data={"message":"Get method not allowed"})

    def post(self,request):
        instance = request.data
        for i in instance:
            if 'student' not in i.keys():
                continue
            try:                
                instance1 = Attendance.objects.get(lecture = i['lecture'], student = int(i['student']))
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

class RangeAttendanceDownload(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    def post(self,request):
        try:
            instance1 = Attendance.objects.filter(subject = int(request.data['subject'])).filter(lecture__batch = int(request.data['batch'])).filter(lecture__teacher__user__id = request.user.id).order_by('student__user__sap_id','lecture__date')
            # .filter(lecture__teacher__user__id = request.user.id).order_by('student__user__sap_id','lecture__date')
            # .filter(lecture__batch = int(request.data['batch']))
            # .filter(lecture__teacher__user__id = request.user.id).order_by('student__user__sap_id','lecture__date')
            print(instance1)
            
                        
            attendan = []
            sy,sm,sd = request.data['start'].split('-')
            startdate =  datetime.datetime(int(sy), int(sm), int(sd)).date()
            ey,em,ed = request.data['end'].split('-')
            end_date =  datetime.datetime(int(ey), int(em), int(ed)).date()
            print(sd,sm,sy)
            
            
            lectures = Lecture.objects.filter(date__gte = startdate , date__lte = end_date ).filter(subject = request.data['subject'],batch = request.data['batch'],teacher__user__id = request.user.id)
            no_of_lecs = len(lectures)
            
            sap_list=[]
            sap_score = []
            i = 0
            
            for j in instance1:
                # print(j.lecture.date)
                if(j.lecture.date >= startdate and j.lecture.date <= end_date ):
                    attendan.append(j)
                    
            for j in attendan:
                # print(f'{j} - '+ str(j.lecture.date))
                
                if j.student.user.sap_id in sap_list and j.present == True:
                    sap_score[i-1] += 1
                elif j.student.user.sap_id in sap_list and j.present == False:
                    pass
                else:
                    sap_list.append(j.student.user.sap_id)
                    if j.present == True:
                        sap_score.append(1)
                    else:
                        sap_score.append(0)
                    i += 1
            attendance_final = []        
            for i in range(len(sap_list)):
                attendance_final.append({'SAP' : sap_list[i], 'Full Name' : User.objects.get(sap_id = sap_list[i]).getfullname() , 'Attendance' : sap_score[i] , 'Total Lectures': no_of_lecs})
                print(f'{sap_list[i]} -{sap_score[i]} - {User.objects.get(sap_id = sap_list[i]).getfullname()}')
                i += 1    
            # print(attendan.student.user.sap_id)                  
            print(attendance_final)
            #creating the CSV file :
            
            fields = ["SAP","Full Name","Attendance","Total Lectures"]
            
            filename = f"attendancefiles/{request.data['batch']}_{startdate}_To_{end_date}_AttendanceList"   
            
            with open(filename,'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = fields) 
                writer.writeheader() 
                writer.writerows(attendance_final) 
                  
            with open(filename) as csvfile:
                response = HttpResponse(csvfile, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
                return response
        except Exception as e:
            return Response(data ={'message' : str(e)}, status = status.HTTP_400_BAD_REQUEST)
            # return Response({'message' : 'uhohh'}, status = status.HTTP_400_BAD_REQUEST)
        
    
    
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
    
class TeacherBatchAPI(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsTeacher]
    def get(self, request):
        teacherbatch = TeacherBatchSerializer(TeacherBatch.objects.filter(teacher = Teacher.objects.get(user = request.user.id).id), many = True)
        batch_array = []
        for i in teacherbatch.data:
            if i['batch']['class_teacher'] == {}:
                cTeacher = "Not defined"
            else:
                cTeacher = User.objects.get(id  = i['batch']['class_teacher']['user']['id']).getfullname()
            batch_array.append(
                {'id':i['batch']['id'],
                        'semester':i['batch']['semester'],
                        'year':i['batch']['year'],
                        'name':i['batch']['name'],
                        'number_of_students':i['batch']['number_of_students'],
                        'class_teacher' : cTeacher,
                        'department' : i['batch']['department']['name']
                        }
            )
        # batch_array = [{'id':i['batch']['id'],
        #                 'semester':i['batch']['semester'],
        #                 'year':i['batch']['year'],
        #                 'name':i['batch']['name'],
        #                 'number_of_students':i['batch']['number_of_students'],
        #                 'class_teacher' : cTeacher,
        #                 'department' : i['batch']['department']['name']
        #                 }
        #                for i  in teacherbatch.data]
        return Response(batch_array)
    
class BatchDataAPI(APIView):
    def post(self, request):
        try:
            # print(Batch.objects.get(id = request.data['batch']))
            batch = newBatchSerializer(Batch.objects.get(id = request.data['batch'])).data
            student_array = [{'id':i['id'],
                              'sap_id':i['user']['sap_id'],
                            #   'name' : User.objects.get(id  = i['user']['id']).getfullname()
                            'name': i['user']['first_name']+" "+ i['user']['last_name']
                              } 
                             for i in batch['students']]
            return Response(student_array)
        except KeyError:
            return Response(data= {'error':{"batch":["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data= {'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# class DownloadAttendanceRange(GenericAPIView):
#     serializer_class = AttendanceSerializer
#     queryset = Attendance.objects.all()
#     def post(self,request):

#         attendances = Attendance.objects.filter(student = Student.objects.get(id = request.data['student'])).filter(subject = request.data['subject'])
#         fromDate = request.data['from']
#         toDate = request.data['to']
#         count = 0
#         for attendance in attendances:
#             if attendance.present:
#                 count +=1
#             print(attendances.count())
#             print (attendance.lecture.date)
#             print(count)
#             print(attendance.subject)
#             per = (attendances.count()/count)*100
#             print('attendance % = ',per)
#             print(attendance.date_time)
#         lec_list = []
#         lectures = Lecture.objects.filter(date__range = [fromDate,toDate],teacher =Teacher.objects.get(user =  request.user.id).id,batch = request.data['batch'],subject = request.data['subject'])
#         print(lectures)       
#         for lecture in lectures:
            
#             lec_list.append(
#                 lecture
#             )
        
#         # for lecture in lec_list:
#         #     print(lecture.teacher,lecture.subject)
#         attendance_list= {}
#         for lecture in lectures:
#             # print(lecture.teacher)
#             attendances = Attendance.objects.filter(lecture = lecture.id).order_by('id')
#             for attendance in attendances:
#                 print(attendance)
#                 if attendance.student.user.sap_id not in attendance_list:
#                     print(attendance.student.user.sap_id,"Not found")
#                     if attendance.present:
#                         attendance_list[attendance.student.user.sap_id] = [1,(1/len(lec_list)*100)]
#                     else:
#                         attendance_list[attendance.student.user.sap_id] = [0,0.0]
#                 else:
#                     if attendance.present:
#                         attendance_list[attendance.student.user.sap_id] = [attendance_list[attendance.student.user.sap_id][0]+1, (attendance_list[attendance.student.user.sap_id][0]+1)/len(lec_list)*100 ]
#                     # else:
#                     #     attendance_list[attendance.student.user.sap_id][0] += 1
                    
#         print(attendance_list)
        
#         # {
#         #     "student":155,
#         #     "subject":2,
#         #     "from": "2023-05-07",
#         #     "to" : "2023-05-18",
#         #     "batch":9           
#         # }

#         return Response('hello')    

class MailAttendanceAPI(GenericAPIView):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def post(self,request):
        try:
            user = request.user
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
                subject = 'Here is your file'
                message = f'File : {filename}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                mail = send_mail( subject, message, email_from, recipient_list )
                return Response({'status': 200,'message' : 'Please Check Your Mail, File has been sent to your mail'})
        except KeyError:
            return Response(data= {'error':{"lecture":["This field is required."]}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data= {'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class InputFile(GenericAPIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    # serializer_class = TeacherBatchSerializer
    def post(self,request):
        file = request.FILES.getlist('files')
        
        for i in range(len(file)):
            # print(file[i]) 
            CustomSapDump(file[i])
               
            
        return Response(status = status.HTTP_200_OK)    
    
    
