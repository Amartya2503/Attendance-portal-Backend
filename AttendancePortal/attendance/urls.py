from django.urls import path
from .views import *

urlpatterns = [
    path('lecture/', LectureAPI.as_view(), name  = 'lecture'),
    path('lecture/<int:id>',EDLectureAPI.as_view(), name = 'Lecture'),
    path('batch/', BatchAPI.as_view(), name  = 'batch'),
    path('lecture-attendance/',AttendanceAPI.as_view(), name = 'attendance'),
    path('download-attendance/', DownloadAttendanceAPI.as_view(), name = 'download_attendance'),
    path('assigned-teacher-lecture/', AssignedTeacherLectureAPI.as_view(), name = 'assignedteacherlecture'),
    path('teachers-batch/', TeacherBatchAPI.as_view(), name = 'teacherbatch'),
    path('batch-data/', BatchDataAPI.as_view(), name = 'batch-data'),
    # path('download-attendance-range/',DownloadAttendanceRange.as_view(),name='download-attendance-range')
    path('download-attendance-range/',RangeAttendanceDownload.as_view(),name='download-attendance-range'),
]