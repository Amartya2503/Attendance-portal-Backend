from django.db import models
from accounts.models import Teacher, Student, Subject, Department
import datetime 

class Batch(models.Model):
    semester = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField(default=datetime.date.today().year)
    name = models.CharField(max_length=55)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True,blank= True)
    students = models.ManyToManyField(Student)
    number_of_students = models.IntegerField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def define(self):
        yearname = "" #to add the no. of students to get autometically filled
        semester = self.semester
        if semester <= 2:   
            yearname = "FE"
        elif semester <= 4:
            yearname = "SE"
        elif semester <= 6:
            yearname = "TE"
        elif semester <= 8:
            yearname = "BE"
        return yearname + "_" + self.name
    
    @staticmethod
    def yearnameToYear(yearname):
        if yearname == "FE":
            year = 1
        elif yearname == "SE":
            year = 2
        elif yearname == "TE":
            year = 3
        elif yearname == "BE":
            year = 4
        return year
    
    def __str__(self):
        yearname = "" #to add the no. of students to get autometically filled
        semester = self.semester
        if semester <= 2:
            yearname = "FE"
        elif semester <= 4:
            yearname = "SE"
        elif semester <= 6:
            yearname = "TE"
        elif semester <= 8:
            yearname = "BE"
        return yearname + "_" + self.name + "-id- " + str(self.pk)
    
class Lecture(models.Model):
    room_number = models.CharField(max_length=32, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_lecture')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='student_leture')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_leture')
    startTime = models.TimeField(auto_now=False, auto_now_add=False)
    endTime = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(auto_now=False, auto_now_add=False)
    note = models.TextField(max_length=250, null=True, blank=True)
    attendance_taken = models.BooleanField(default=False)
       
    def __str__(self):
        return str(self.batch) + " " + self.subject.name + " " + str(self.getShortTimeString()) + "-id- " + str(self.pk)

    def getTimeString(self):
        return self.startTime.strftime("%H:%M:%S") + " - " + self.endTime.strftime("%H:%M:%S")

    def getShortTimeString(self):
        return self.startTime.strftime("%I:%M") + "-" + self.endTime.strftime("%I:%M")

    def getDateTimeString(self):
        return self.date.strftime("%d-%m-%Y") + " : " + self.getTimeString()

class Attendance(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecture_attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lecture_subject')
    # date_time = models.DateTimeField(auto_now_add=True,blank=True)
    present = models.BooleanField(default= False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,related_name='Attendance_subject',default=1)

    def isPresent(self):
        if self.present == True:
            return "Present"
        else:
            return "AB"
    
    def __str__(self):
        return str(self.student.user.sap_id)+ " " + str(self.lecture.batch)+ " " + str(self.lecture.subject) + " " + self.isPresent() + "-id- " + str(self.pk)

class TeacherBatch(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_batch')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_teacher_assigned')

    def __str__(self):
        return str(self.teacher.user.first_name) +' '+str(self.batch.name)
    
# theis is to keep a track of a student attending a perticular subject 
# class StudentSubject(models.Model):
#     # student