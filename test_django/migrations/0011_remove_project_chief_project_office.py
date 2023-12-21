# Generated by Django 4.2.5 on 2023-11-22 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0010_remove_project_office_project_chief'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='chief',
        ),
        migrations.AddField(
            model_name='project',
            name='office',
            field=models.ForeignKey(db_column='office', default='Золотое яблоко', help_text='Введите название офиса', on_delete=django.db.models.deletion.CASCADE, to='test_django.office', verbose_name='Офис'),
        ),
    ]
