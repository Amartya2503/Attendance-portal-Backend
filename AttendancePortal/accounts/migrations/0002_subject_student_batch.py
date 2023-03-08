# Generated by Django 4.1.7 on 2023-03-05 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='subject',
            fields=[
                ('subject_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sap_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studentid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='batch',
            fields=[
                ('batch_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=115)),
                ('students', models.ManyToManyField(to='accounts.student')),
            ],
        ),
    ]