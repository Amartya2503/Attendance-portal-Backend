# Generated by Django 4.1 on 2023-04-06 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_middle_name'),
        ('attendance', '0003_alter_batch_class_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='department',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='accounts.department'),
        ),
    ]