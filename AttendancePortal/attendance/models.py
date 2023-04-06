from django.db import models
from accounts.models import Teacher, Student, Subject, Department
import datetime 

class Batch(models.Model):

    semester = models.PositiveSmallIntegerField()
    year = models.PositiveIntegerField(default=datetime.date.today().year)
    name = models.CharField(max_length=55,primary_key=True)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, default=None)
    students = models.ManyToManyField(Student)
    number_of_students = models.IntegerField()
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)

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
        return yearname + "_" + self.name
    
class Lecture(models.Model):
    room_number = models.CharField(max_length=32, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_lecture')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='student_leture')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_leture')
    startTime = models.TimeField(auto_now=False, auto_now_add=False)
    endTime = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(auto_now=False, auto_now_add=False)
    note = models.TextField(max_length=250, null=True, blank=True)
    attendance_taken = models.BooleanField(default=False)
       
    def __str__(self):
        return str(self.batch) + " " + self.subject.name + " " + str(self.getShortTimeString())

    def getTimeString(self):
        return self.startTime.strftime("%H:%M:%S") + " - " + self.endTime.strftime("%H:%M:%S")

    def getShortTimeString(self):
        return self.startTime.strftime("%I:%M") + "-" + self.endTime.strftime("%I:%M")

    def getDateTimeString(self):
        return self.date.strftime("%d-%m-%Y") + " : " + self.getTimeString()

class BatchStudent(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_student')
    student =  models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_batch')

class SubjectTeacher(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_teacher')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_subject')

    def __str__(self):
        return str(self.teacher) + " " + str(self.subject) + " " + str(self.div)

class Attendance(models.Model):

    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecture_attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lecture_subject')
    date_time = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default= False)

    def isPresent(self):
        if self.present == True:
            return "Present"
        else:
            return "AB"
    
    def __str__(self):
        return str(self.student.user.sap_id)+ " " + str(self.lecture.batch)+ " " + str(self.lecture.subject) + " " + self.isPresent()
    