# Generated by Django 3.1.1 on 2021-06-08 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210608_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='result_json',
            field=models.TextField(),
        ),
    ]