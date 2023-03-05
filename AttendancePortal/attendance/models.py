from django.db import models
from accounts.models import User,student ,subject,teacher


# Create your models here.

class batch(models.Model):
    batch_name = models.CharField(max_length=55,primary_key=True)
    students = models.ManyToManyField(student)
    number_of_students = models.IntegerField()
    department = models.CharField(max_length=125)

    def __str__(self):
        return self.batch_name


class lecture(models.Model):
    lec_id = models.IntegerField(primary_key = True)
    teacher_id = models.ForeignKey(teacher , on_delete=models.CASCADE)
    batch_name = models.ForeignKey(batch, on_delete=models.CASCADE)
    sub_id = models.ForeignKey(subject, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=250)

    def __str__(self):
        return self.batch_name + " " + self.note