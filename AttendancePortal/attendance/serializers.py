from typing import Self
from rest_framework import serializers
from accounts.serializers import TeacherSerializer, StudentSerializer, DepartmentSerializer, SubjectSerializer
from accounts.models import Teacher, Student, Department, Subject
from attendance.models import Attendance, Batch, Lecture

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['class_teacher'] = TeacherSerializer(
            Teacher.objects.get(pk=data['class_teacher'])).data
        data['students'] = StudentSerializer(
            instance.students.all(), many=True).data
        data['department'] = DepartmentSerializer(
            Department.objects.get(pk=data['department'])).data
        return data

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['teacher'] = TeacherSerializer(
            Teacher.objects.get(pk=data['teacher'])).data
        data['batch'] = BatchSerializer(
            Batch.objects.get(pk=data['batch'])).data
        data['subject'] = SubjectSerializer(
            Subject.objects.get(pk=data['subject'])).data
        return data

    def create(self, validated_data):
        batch = BatchSerializer(validated_data['batch']).data
        lecture = Lecture.objects.create(**validated_data)
        for i in batch['students']:
            serializer = AttendanceSerializer(data = {'lecture' : lecture.id, 'student': i['id']})
            if serializer.is_valid():
                serializer.save()
        return lecture

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['lecture'] = LectureSerializer(
           Lecture.objects.get(pk=data['lecture'])).data
        data['student'] = StudentSerializer(
            Student.objects.get(pk=data['student'])).data
        return data