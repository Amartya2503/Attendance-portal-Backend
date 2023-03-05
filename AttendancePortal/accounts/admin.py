from django.contrib import admin
from .models import * #User , student
# Register your models here.

admin.site.register(User)
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(subject)
# admin.site.register(batch)
