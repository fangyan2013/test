# Generated by Django 3.1.1 on 2021-06-08 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_execution_status_s_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='execution_status',
            name='status',
            field=models.TextField(),
        ),
    ]
