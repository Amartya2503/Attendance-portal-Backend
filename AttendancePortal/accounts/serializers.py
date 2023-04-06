from rest_framework import serializers
from .models import User, Subject, Student, Teacher, Department

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['department'] = DepartmentSerializer(
            Department.objects.get(pk=data['department'])).data
        return data
        

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user'])).data
        return data

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = UserSerializer(
            User.objects.get(pk=data['user'])).data
        data['subjects'] = UserSerializer(
            Subject.objects.get(pk=data['subjects'])).data
        return data

