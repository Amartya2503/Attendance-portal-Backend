import csv
import importlib  

from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q
from accounts.models import Teacher, Student, Subject, User,Department
# accounts = importlib.import_module('AttendancePortal.accounts.models')
# from accounts import Teacher
from attendance.models import Batch,TeacherBatch
from datetime import datetime, timedelta, date
import math
import os

current_year = date.today().year

if date.today().month < 6:
    current_sem = "even"
else:
    current_sem = "odd"
# file name format : BE_Batchname_Department_ClassTeacherSAP.csv
def CustomSapDump(file):
    print(file)
    try:  
        uploaded_file = file
        filename = str(file)
        list_name = str(filename).split("_")
        print(list_name)
        if len(list_name) == 4:
            yearname, division,department,classteacher = str(filename).split("_")
            department= int(department)
            teacher_SAP = int(classteacher.split('.')[0])
        elif len(list_name) == 3:
            yearname, division,department = str(filename).split("_")
            department = int(department.split(".")[0])
            teacher_SAP = 19210161 #assigning defult pranit bari sir's Sap Id as Sap not provided in the file name
            print("assigning defult pranit bari sir's Sap Id as Sap not provided in the file name")               
        else:
            print(len(list_name))
            raise Exception("there is an issue in the file name ")                 
        overwrite= True
        reverse_names = False
        try:
            teacher = Teacher.objects.get(user = User.objects.get(sap_id = teacher_SAP))
        except Teacher.ObjectDoesNotExist:
            print("no teacher is in the database with sap id ",teacher_SAP," thus assigning defauly teacher sap ",19210161)
            teacher = Teacher.objects.get(user = User.objects.get(sap_id = 19210161))
            
        
        print(type(file))       
        year = Batch.yearnameToYear(yearname)
        #yeartoYearname is a function ------ 

        if date.today().month < 6:
            semester = year * 2
        elif date.today().month > 6:
            semester = year * 2 - 1

        div_exists = Batch.objects.filter(semester=semester, name=division,department = department).exists()
        print(div_exists)
        print(yearname,department,classteacher,teacher_SAP)
        if div_exists and not overwrite:
            raise Exception("Div already exists, set overwrite to True to overwrite")
        elif div_exists:
            div = Batch.objects.get(semester=semester, name=division,department = department)
            if div.class_teacher is None and teacher :
                div.class_teacher = teacher
            else:
                print("no teacher was found")
                                    
        else:
            if teacher_SAP:
                # names = classteacher.strip().split(' ')
                teacher = Teacher.objects.get(user=User.objects.get(sap_id = teacher_SAP))
                div = Batch.objects.create(semester=semester, name=division,department = int(department))
                div.class_teacher = teacher
                div.save()
            else:
                div = Batch.objects.create(semester=semester,  name=division,department = Department.objects.get(id = department))
                div.save()
                
        count = 0
        if isinstance(uploaded_file, InMemoryUploadedFile) and uploaded_file.content_type == 'text/csv':
            # Read the contents of the uploaded CSV file
            file_contents = uploaded_file.read().decode('utf-8')  
                        
            # Create a CSV reader using the StringIO object
            csv_io = io.StringIO(file_contents)
            csv_reader = csv.reader(csv_io)
            
            # Iterate through the CSV rows
            for row in csv_reader:
                if len(row[1]) and len(row[2]):
                    name = row[2].lower()
                    sap = int(row[1])
                    try:
                        user = User.objects.get(sap_id=sap)
                        user.is_student = True
                        found = True
                    except User.DoesNotExist:
                        user = User.objects.create(sap_id=sap, password='pass@123',email = (str(sap)+'@mail.com'))
                        user.set_password('pass@123')
                        user.is_student = True
                        found = False

                    if (not found) or overwrite:
                        names = name.split(' ')
                        names = [name.capitalize() for name in names]
                        if reverse_names:
                            if len(names) > 2:
                                user.first_name = names[1]
                                user.middle_name = " ".join(names[2:])
                                user.last_name = names[0]
                            elif len(names) == 2:
                                user.first_name = names[1]
                                user.last_name = names[0]
                            else:
                                user.first_name = name
                                user.last_name = ""
                        else:
                            if len(names) > 2:
                                user.first_name = names[0]
                                user.middle_name = " ".join(names[1:-1])
                                user.last_name = names[-1]
                            elif len(names) == 2:
                                user.first_name = names[0]
                                user.last_name = names[1]
                            else:
                                user.first_name = name
                                user.last_name = "" 
                        user.save()

                    if not found:
                        student = Student.objects.create(user=user)
                        print("created student",student.user.first_name)
                        count += 1
                    else:
                        student = Student.objects.get(user=user)
                        print("student found",student.user.first_name)
                        count += 1 

                    # StudentDivision.objects.get_or_create(student=student, division=div)
                    # print(student)
                    div.students.add(student)
                    div.save()
            div.number_of_students = count
            div.save()
        else:
            print("Uploaded file is not a CSV file.")       
    except Exception as e:
        raise Exception("the file name provided is not acceptable or the name format is incorrect",e)
    
def SAPDump(path, div_name, overwrite=False, reverse_names=False, classteacher=None):
    #required format of input from shell now becomes SE_A_COMP
    # instead of SE_A earlier

    yearname, division,department = div_name.split("_")
    department = int(department)
    print(department)
    print(type(department))

    year = Batch.yearnameToYear(yearname)
    #yeartoYearname is a function ------ 

    if date.today().month < 6:
        semester = year * 2
    elif date.today().month > 6:
        semester = year * 2 - 1

    div_exists = Batch.objects.filter(semester=semester, name=division,department = department).exists()
    if div_exists and not overwrite:
        raise Exception("Div already exists, set overwrite to True to overwrite")
    elif div_exists:
        div = Batch.objects.get(semester=semester, name=division,department = department)
    else:
        if classteacher:
            names = classteacher.strip().split(' ')
            teacher = Teacher.objects.get(user=User.objects.get(first_name=names[0], last_name=names[1]))
            div = Batch.objects.create(semester=semester, name=division,department = int(department))
            div.class_teacher = teacher
            div.save()
        else:
            div = Batch.objects.create(semester=semester,  name=division,department = Department.objects.get(id = department))
            div.save()

    count = 0
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if len(row[1]) and len(row[2]):
                name = row[2].lower()
                sap = int(row[1])
                try:
                    user = User.objects.get(sap_id=sap)
                    user.is_student = True
                    found = True
                except User.DoesNotExist:
                    user = User.objects.create(sap_id=sap, password='pass@123',email = (str(sap)+'@mail.com'))
                    user.set_password('pass@123')
                    user.is_student = True
                    found = False

                if (not found) or overwrite:
                    names = name.split(' ')
                    names = [name.capitalize() for name in names]
                    if reverse_names:
                        if len(names) > 2:
                            user.first_name = names[1]
                            user.middle_name = " ".join(names[2:])
                            user.last_name = names[0]
                        elif len(names) == 2:
                            user.first_name = names[1]
                            user.last_name = names[0]
                        else:
                            user.first_name = name
                            user.last_name = ""
                    else:
                        if len(names) > 2:
                            user.first_name = names[0]
                            user.middle_name = " ".join(names[1:-1])
                            user.last_name = names[-1]
                        elif len(names) == 2:
                            user.first_name = names[0]
                            user.last_name = names[1]
                        else:
                            user.first_name = name
                            user.last_name = "" 
                    user.save()

                if not found:
                    student = Student.objects.create(user=user)
                    count += 1
                else:
                    student = Student.objects.get(user=user)
                    count += 1 

                # StudentDivision.objects.get_or_create(student=student, division=div)

                div.students.add(student)
                div.save()
                # print(user.id)

                #this field will add the student to the respective batches 

                print(student)
        div.number_of_students = count
        div.save()
            
    csvFile.close()


# def WorkLoadDump(path, semester=current_sem):
#     with open(path, 'r', encoding='utf-8-sig') as csvFile:
#         reader = csv.reader(csvFile)
#         yr = ''
#         sub = ''
#         for row in reader:
#             if row[0] != '':
#                 yr = row[0]
#             if row[1] != '':
#                 sub = row[1]
#             if row[2] != '' and row[3] != '':
#                 div_names = row[2].split('&')
#                 teacher_names = [name.strip().split(' ') for name in row[3].split('/')]
#                 year = Div.yearnameToYear(yr.upper())
#                 if semester == "even":
#                     sem = year * 2
#                 else:
#                     sem = year * 2 - 1
#                 subject, _ = Subject.objects.get_or_create(name=sub, semester=sem)
#                 all_divs = Div.objects.filter(semester=sem, calendar_year=current_year)
#                 divs = all_divs.filter(division__in=div_names)
#                 users = []
#                 for name in teacher_names:
#                     try:
#                         users.append(AppUser.objects.get(first_name=name[0]+ " " +name[-1]))
#                     except AppUser.DoesNotExist:
#                         print("\033[91m{}\033[00m" .format(name[0] + " " + name[1] + " not found"))

#                 teachers = Teacher.objects.filter(user__in=users)
#                 for teacher in teachers:
#                     for div in divs:
#                         if not all_divs.filter(division=div.division + sub).exists():
#                             SubjectTeacher.objects.get_or_create(subject=subject, div=div, teacher=teacher)
#                             print(subject, div, teacher)
#                         else:
#                             elective_div = all_divs.get(division=div.division + sub)
#                             SubjectTeacher.objects.get_or_create(subject=subject, div=elective_div, teacher=teacher)
#                             print(subject, elective_div, teacher)


def createTeacher(id, f_name, l_name, spec="Computer Engineering"):

    try:
        instance = User.objects.get(sap_id = id)
        Teacher.objects.get(user = instance.sap_id)
        
    except User.DoesNotExist:
    
        user = User.objects.create(sap_id=id, password="pass@123")
        user.set_password('pass@123')
        user.first_name = f_name
        user.last_name = l_name
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user,specialization=spec)
        print("created User and Teacher ",user,teacher)
    except Teacher.DoesNotExist:
        instance = User.objects.get(sap_id = id)
        teacher = Teacher.objects.create(user=user,specialization=spec)
        print("created teacher : ",teacher)
            
def mycreateTeacher(path,department):

    if department ==1 :
        specialisation = 'Computer engineering'
    elif department == 2 :
        specialisation = 'Information Technology'
    else:
        specialisation = 'unknown'
    
    with open(path,'r') as csvFlie:
        reader = csv.reader(csvFlie)
        for row in reader:
            try:
                id = int(row[0])
            except:
                id = int(row[0][3:],10)
            name = row[1]
            names = name.split(' ')
            names = [name.capitalize() for name in names]
            print(id," ", names)
            try:
                instance = User.objects.get(sap_id = id)
                Teacher.objects.get(user = instance)
                print("Teacher and user with given id exist")
            except User.DoesNotExist:
            
                user = User.objects.create(sap_id=id, password="pass@123")
                user.set_password('pass@123')
                user.first_name = names[0]
                user.last_name = names[1]
                user.is_teacher = True
                user.email = f"{names[0]}@mail.com"
                user.save()
                teacher = Teacher.objects.create(user=user,specialization=specialisation)
                print("created User and Teacher ",user,teacher)
            except Teacher.DoesNotExist:

                instance = User.objects.get(sap_id = id)
                teacher = Teacher.objects.create(user=user,specialization=specialisation)
                print("created teacher : ",teacher)


def yearnameToSem(yearname):
    if yearname == "FE":
        year = 1
    elif yearname == "SE":
        year = 2
    elif yearname == "TE":
        year = 3
    elif yearname == "BE":
        year = 4
    else:
        year = 0
    return year

def createSubjects(path):
    with open (path,'r') as csvFile:
        reader = csv.reader(csvFile)
        dept = Department.objects.get(id = 1)
        
        for row in reader:
            name = row[1]
            sem = yearnameToSem(row[0])
            sem = sem*2 -1
            # dept_name = Department.objects.filter(id = dept)
            subject = Subject.objects.filter(name = name).filter(Q(semester = sem) | Q(semester = sem+1)).exists()
            if subject is not True:
                print("this subject dne")
                Subject.objects.create(name = name,semester = sem,department = dept )
            else:
                print("this subject exist")
            print(name,sem,dept.name)                
                
            
            
def assignTeacherBatch(path):
     with open (path,'r') as csvFile:
        reader = csv.reader(csvFile)
                       
        for row in reader:
            # lec_name = row[1] 
            name = row[3]
            names = name.split(" ")
            print(names[0],"  ",names[1])
            
            sem = yearnameToSem(row[0])
            sem = sem*2 -1
                
            batch = Batch.objects.filter(Q(semester = sem) | Q(semester = sem +1)).filter(Q(name__contains = row[1]) | Q(name = row[2])).last()
            # print(batch)
            
            # teacher = Teacher.objects.filter(user__first_name= names[0],user__last_name__contains = names[1]).exists()
            
            teacher = Teacher.objects.filter(user__first_name__contains = names[0]).last()
            print("Teacher - >",teacher," batch -> ", batch)
            
            # if teacher is not None:
                
            #     teacher = Teacher.objects.filter(user__first_name__contains = names[0],user__last_name__contains = names[1])
            #     print("found teacher ",teacher)
                
            # else:
                
            #     teacher = Teacher.objects.filter(user__first_name__contains = names[0])
            #     print("found teacher ",teacher)
            if teacher is not None and batch is not None:
                    
                teacherBatch = TeacherBatch.objects.filter(teacher = teacher,batch = batch).exists()
                print(teacherBatch)
                if teacherBatch is not False:
                    
                    teacherBatch = TeacherBatch.objects.filter(teacher = teacher,batch = batch)
                    print("teacher batch not exist ",teacher," ",batch)
                    
                else:
                    
                    teacherBatch = TeacherBatch.objects.create(teacher = teacher,batch = batch)
                    print("created teacher lecture relational model",teacherBatch)
                    
            else:
                print(teacher,batch)   
            
def assignTeacherbatch(path):
    with open (path,'r') as csvFile:
        reader = csv.reader(csvFile)
                       
        for row in reader:
            # lec_name = row[1] 
            name = row[3]
            names = name.split(" ")
            sub = row[1]
            print(names[0],"  ",names[1])
            sem = yearnameToSem(row[0])
            sem = sem*2 -1
            
            # batch = Batch.objects.filter(Q(semester = sem) | Q(semester = sem +1)).filter(Q(name__contains = row[1]) | Q(name = row[2])).last()
            
            # print(batch)
            
            subject = Subject.objects.filter(name = sub).filter(semester = sem)
            print(subject[0].id)
            
            teacher = Teacher.objects.filter(user__first_name__contains = names[0]).last()
            print(teacher)
            
            teacher.subjects.add(subject[0].id)
            teacher.save()
            print("added subject ",subject," to teacher ",teacher)
            
            

def dumpWorkLoad(path):
    # with open(path,'r') as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    instance = Batch.objects.filter(name = 'B-BDI')
    teacher =Teacher.objects.filter(user__first_name ='Sridhar',user__last_name = 'Iyer' ).exists()
    
    if teacher  is not True:
        teacher =Teacher.objects.filter(user__first_name ='Sridhar')
    else:
        teacher =Teacher.objects.filter(user__first_name ='Sridhar',user__last_name = 'Iyer' )
    
    sem = yearnameToSem("SE")
    print(sem,instance,teacher)


# def fillPracs(div_name, end1, end2, end3):
#     yearname, division = div_name.split("_")
#     year = Div.yearnameToYear(yearname)

#     if date.today().month < 6:
#         semester = year * 2
#     elif date.today().month > 6:
#         semester = year * 2 - 1

#     div = Div.objects.get(semester=semester, calendar_year=date.today().year, division=division)
#     p1, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
#                                       division=division + "1")
#     p2, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
#                                       division=division + "2")
#     p3, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
#                                       division=division + "3")
#     p4, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
#                                       division=division + "4")

#     students = Student.objects.filter(div=div)
#     for student in students:
#         if student.sapID <= end1:
#             print(StudentDivision.objects.get_or_create(student=student, division=p1)[0])
#         elif student.sapID <= end2:
#             print(StudentDivision.objects.get_or_create(student=student, division=p2)[0])
#         elif student.sapID <= end3:
#             print(StudentDivision.objects.get_or_create(student=student, division=p3)[0])
#         else:
#             print(StudentDivision.objects.get_or_create(student=student, division=p4)[0])


# def fillPracs2(path, div_name, new_div_name):
#     yearname, division = div_name.split("_")
#     year = Div.yearnameToYear(yearname)

#     if date.today().month < 6:
#         semester = year * 2
#     elif date.today().month > 6:
#         semester = year * 2 - 1
#     div = Div.objects.get(semester=semester, calendar_year=date.today().year, division=division)
#     p1, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
#                                       division=new_div_name)

#     with open(path, 'r', encoding='utf-8-sig') as csvFile:
#         reader = csv.reader(csvFile)
#         for row in reader:
#             if row[0] != '':
#                 sap = row[0]
#                 # print(sap)
#                 try:
#                     student = Student.objects.get(sapID=sap)
#                     StudentDivision.objects.get_or_create(student=student, division=p1)
#                     print(student.user.first_name, student.user.last_name, student.sapID)
#                 except:
#                     print("\033[91m{}\033[00m" .format(sap + " not found"))


# def TheoryElective(path, div_name, new_div_name):
#     yearname , division = div_name.split("_")
#     year = Div.yearnameToYear(yearname)

#     if date.today().month < 6:
#         semester = year * 2
#     elif date.today().month > 6:
#         semester = year * 2 - 1

#     div = Div.objects.get(semester=semester, calendar_year=date.today().year, division=division)
#     p1, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
#                                       division=new_div_name)

#     with open(path, 'r', encoding='utf-8-sig') as csvFile:
#         reader = csv.reader(csvFile)
#         for row in reader:
#             if row[1] != '':
#                 sap = row[0]
#                 # print(sap)
#                 try:
#                     student = Student.objects.get(sapID=sap)
#                     StudentDivision.objects.get_or_create(student=student, division=p1)
#                     print(student.user.first_name, student.user.last_name, student.sapID)
#                 except:
#                     print("\033[91m{}\033[00m" .format(sap + " not found"))
    


# def TeacherDump(path, spec="Computer Engineering"):
#     with open(path, 'r') as csvFile:
#         reader = csv.reader(csvFile)
#         for row in reader:
#             if row[0] != '':
#                 id = row[0]
#                 f_name = row[1]
#                 user = AppUser.objects.create(username=id, password="pass@123")
#                 user.set_password('pass@123')
#                 user.first_name = f_name
#                 user.is_teacher = True
#                 user.save()
#                 teacher = Teacher.objects.create(user=user, teacherID=id, specialization=spec)
#                 print(teacher)

# TO RUN THIS SCRIPT -
#
# python manage.py shell
#
# from SAP import dump
#
# AVAILABLE FUNCTIONS USAGE EXAMPLES -
# reads names in format "FirstName MiddleName LastName", classteacher is left Null and doesn't overwrite old entries
# dump.SAPDump("SAP/TEA.csv", "TE_A")
#
# reads names in format "LastName FirstName MiddleName", classteacher is Sindhu Nair and will overwrite old
# conflicting entries
# dump.SAPDump("SAP/TEA.csv", "TE_A", overwrite=True, reverse_names=True, classteacher="Sindhu Nair")
# 
# dump teachers data
# dump.TeacherDump("SAP/Teachers.csv")
#
# populates current semester (odd for june to dec and even for jan to may) with teacher workload data
# dump.WorkLoadDump("SAP/WorkLoad.csv")
#
# creates a teacher with id and username 19210161, first name Pranit and last name Bari
# dump.createTeacher(19210161, "Pranit", "Bari")
#
# creates 4 practical batches, "TE_A1" upto 20, "TE_A2" upto 41, "TE_A3" upto 59 and "TE_A4" for remaining
# dump.fillPracs("TE_A", 60004170020, 60004170041, 60004170059)
# 
# For pracs batches (TE and BE)
# dump.fillPracs2("SAP/TE_A1","TE_A","A1")
