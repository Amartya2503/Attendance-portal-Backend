from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Attendance)
admin.site.register(Lecture)
admin.site.register(Batch)
admin.site.register(TeacherBatch)