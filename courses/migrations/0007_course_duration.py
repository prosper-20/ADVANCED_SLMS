# Generated by Django 4.2.8 on 2024-06-20 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_code_course_image_course_semester_course_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.TextField(default='12 weeks'),
        ),
    ]
