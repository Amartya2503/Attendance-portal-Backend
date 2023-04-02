from django.contrib import admin
from .models import * #User , student
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
# admin.site.register(batch)
admin.site.register(Batch)
admin.site.register(Lecture)
admin.site.register(StudentBatchRlation)
