from django.urls import path
from .views import *

urlpatterns = [
    path('lecture/', LectureAPI.as_view())
]