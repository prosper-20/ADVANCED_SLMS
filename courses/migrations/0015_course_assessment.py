# Generated by Django 4.2.8 on 2024-08-12 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_alter_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='assessment',
            field=models.URLField(blank=True, null=True),
        ),
    ]
