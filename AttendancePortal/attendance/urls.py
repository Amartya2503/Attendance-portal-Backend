from django.urls import path
from .views import *

urlpatterns = [
    path('lecture/', LectureAPI.as_view(), name  = 'lecture'),
    path('batch/', BatchAPI.as_view(), name  = 'batch')
]