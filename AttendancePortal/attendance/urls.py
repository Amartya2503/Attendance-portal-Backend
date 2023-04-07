from django.urls import path
from .views import *

urlpatterns = [
    path('lecture/', LectureAPI.as_view(), name  = 'lecture'),
    path('batch/', BatchAPI.as_view(), name  = 'batch'),

    path('createattendance/',CreateAttendance.as_view(), name = 'createAttendance'),
]