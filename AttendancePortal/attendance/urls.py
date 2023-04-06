from django.urls import path
from .views import *

urlpatterns = [
    path('hello/',hello.as_view(),name ="testview"),
    
]