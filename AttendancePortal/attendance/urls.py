from django.urls import path
from .views import *

urlpatterns = [
    path('lecture/', LectureAPI.as_view(), name  = 'lecture'),
    path('batch/', BatchAPI.as_view(), name  = 'batch'),
    path('lecture-attendance/',AttendanceAPI.as_view(), name = 'attendance'),
    path('download-attendance/', DownloadAttendanceAPI.as_view(), name = 'download_attendance'),
    path('assigned-teacher-lecture', AssignedTeacherLectureAPI.as_view(), name = 'assignedteacherlecture'),
]