# Generated by Django 4.2.4 on 2023-10-16 07:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_task_category_alter_task_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 16, 7, 19, 18, 150767)),
        ),
    ]