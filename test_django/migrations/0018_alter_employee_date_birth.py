# Generated by Django 4.2.5 on 2023-12-14 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0017_alter_project_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_birth',
            field=models.DateField(help_text='Введите дату рождения', null=True, verbose_name='Дата рождения'),
        ),
    ]