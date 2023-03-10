# Generated by Django 4.1.7 on 2023-03-05 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_rename_sap_id_student_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='batch',
            fields=[
                ('batch_name', models.CharField(max_length=55, primary_key=True, serialize=False)),
                ('number_of_students', models.IntegerField()),
                ('department', models.CharField(max_length=125)),
                ('students', models.ManyToManyField(to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='lecture',
            fields=[
                ('lec_id', models.IntegerField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('note', models.TextField(max_length=250)),
                ('batch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.batch')),
                ('sub_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.subject')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.teacher')),
            ],
        ),
    ]
