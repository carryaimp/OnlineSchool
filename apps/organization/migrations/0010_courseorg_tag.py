# Generated by Django 2.0.2 on 2018-02-20 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_teacher_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='全国知名', max_length=4, verbose_name='机构标签'),
        ),
    ]