from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser




# Create your models here.
class User(AbstractBaseUser):
    sap_id = models.BigIntegerField(unique=True,help_text='Enter your Unique Id')
    first_name = models.CharField(max_length=20, help_text='Enter your First name')
    last_name = models.CharField(max_length=20, help_text='Enter your Last name')
    email = models.EmailField(unique=True, help_text='Enter your email' )
    email_token =  models.CharField(max_length=250, null=True, blank=True)
    password_reset_token = models.CharField(max_length=250, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'sap_id'
    REQUIRED_FIELDS = ['first_name','last_name','email']

    def __str__(self):
        return self.first_name+' '+self.last_name+', '+str(self.sap_id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

#leaving space for creating profile model which will be different for
#for student and teachers
    # .
    # .
    # .
    # .
    # .
# the frontend and app will request the data of Student and using nested serializer we will also provide the data present in the user object of that student such as his name etc


    
class Student(models.Model):
    user = models.ForeignKey("User",related_name="studentid", on_delete=models.CASCADE)
    totalAttendance = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user.sap_id)
    

class Batch(models.Model):

    # from accounts.models import Student

    batch_name = models.CharField(max_length=55,primary_key=True)
    students = models.ManyToManyField(Student)
    number_of_students = models.IntegerField()
    department = models.CharField(max_length=125)

    def __str__(self):
        return self.batch_name +"- "+ self.department
    

class StudentBatchRlation(models.Model):
    batch_id = models.ForeignKey(Batch, related_name="belongs_to", on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name= "student", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.batch_id.batch_name) +" - "+ self.student.user.first_name



class Subject(models.Model):
    subject_id = models.CharField(max_length=25,primary_key=True)
    name = models.CharField(max_length=45,default="CN") 

    def __str__(self):
        return self.name + self.subject_id

class Teacher(models.Model):
    user = models.ForeignKey(User,related_name="is_teacher",on_delete=models.CASCADE)
    # name = models.CharField(max_length=125)  this field is not required as the user has a name
    subjects = models.ManyToManyField(Subject)
    batches = models.ManyToManyField(Batch)

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name


    
class Lecture(models.Model):
    # from accounts.models import Teacher

    lec_id = models.IntegerField(primary_key = True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    batch_name = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # sub_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=250)

    def __str__(self):
        return self.batch_name.batch_name +":  "+ self.note
