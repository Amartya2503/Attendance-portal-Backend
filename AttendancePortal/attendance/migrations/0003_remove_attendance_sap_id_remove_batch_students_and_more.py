# Generated by Django 4.1.7 on 2023-04-02 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='sap_id',
        ),
        migrations.RemoveField(
            model_name='batch',
            name='students',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='sub_id',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='teacher_id',
        ),
    ]
