from django.db import models
from accounts.models import User,Student ,Subject,Teacher


# Create your models here.

class Batch(models.Model):
    batch_name = models.CharField(max_length=55,primary_key=True)
    students = models.ManyToManyField(Student)
    number_of_students = models.IntegerField()
    department = models.CharField(max_length=125)

    def __str__(self):
        return self.batch_name


class Lecture(models.Model):
    lec_id = models.IntegerField(primary_key = True)
    teacher_id = models.ForeignKey(Teacher , on_delete=models.CASCADE)
    batch_name = models.ForeignKey(Batch, on_delete=models.CASCADE)
    sub_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=250)

    def __str__(self):
        return self.batch_name + " " + self.note

class attendance(models.Model):
    lec_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    sap_id = models.ForeignKey(Student,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default= False)
    
