# Generated by Django 3.1.1 on 2021-06-01 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_execution_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='execution_status',
            name='s_id',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
