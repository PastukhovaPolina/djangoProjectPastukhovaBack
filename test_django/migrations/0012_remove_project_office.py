# Generated by Django 4.2.5 on 2023-11-23 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0011_remove_project_chief_project_office'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='office',
        ),
    ]