# Generated by Django 2.0.2 on 2018-02-20 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_course_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='tag',
        ),
    ]
