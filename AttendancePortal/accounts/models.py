from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    sap_id = models.BigIntegerField(unique=True,help_text='Enter your Unique Id')
    first_name = models.CharField(max_length=20, help_text='Enter your First name')
    middle_name = models.CharField(max_length=32, null=True, blank=True, default=None)
    last_name = models.CharField(max_length=20, help_text='Enter your Last name')
    email = models.EmailField(unique=True, help_text='Enter your email' )
    email_token =  models.CharField(max_length=250, null=True, blank=True)
    password_reset_token = models.CharField(max_length=250, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'sap_id'
    REQUIRED_FIELDS = ['first_name','last_name','email']
    
    def getfullname(self):
        if self.middle_name:
            return self.first_name + " " + self.middle_name + " " + self.last_name
        else:
            return self.first_name + " " + self.last_name
    
    def getname(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return str(self.sap_id)

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

class Department(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Subject(models.Model):

    # subject_id = models.CharField(max_length = 225,primary_key=True)
    name = models.CharField(max_length=45) 
    semester = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + '(sem ' + str(self.semester) + ')'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_attendance = models.IntegerField(default=0)

    def __str__(self):
        return  self.user.first_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, null=True, blank=True)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.first_name