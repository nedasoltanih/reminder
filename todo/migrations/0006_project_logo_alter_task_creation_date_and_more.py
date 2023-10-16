# Generated by Django 4.2.4 on 2023-10-16 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_task_creation_date_alter_task_due_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='task',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 7, 48, 14, 930488), editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 7, 48, 14, 930470), help_text='The time and date in which the task must be done!'),
        ),
    ]