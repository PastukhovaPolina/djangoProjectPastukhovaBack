# Generated by Django 4.2.5 on 2023-10-05 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0002_alter_chief_department_alter_chief_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='team',
        ),
        migrations.RemoveField(
            model_name='project',
            name='chief',
        ),
        migrations.RemoveField(
            model_name='project',
            name='employee',
        ),
        migrations.DeleteModel(
            name='Chief',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]