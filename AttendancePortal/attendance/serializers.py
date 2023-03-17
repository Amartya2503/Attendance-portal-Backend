from typing import Self
from rest_framework import serializers

from attendance.models import attendance


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = attendance
        fields = '__all__'