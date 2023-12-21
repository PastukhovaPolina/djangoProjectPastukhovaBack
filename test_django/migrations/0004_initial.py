# Generated by Django 4.2.5 on 2023-10-05 17:37

from django.db import migrations, models
import django.db.models.deletion
import test_django.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('test_django', '0003_remove_employee_team_remove_project_chief_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chief',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите имя', max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Введите фамилию', max_length=100, verbose_name='Фамилия')),
            ],
            options={
                'db_table': 'Chief',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('name', models.CharField(help_text='Введите название отдела', max_length=150, primary_key=True, serialize=False, verbose_name='Имя отдела')),
                ('description', models.TextField(verbose_name='описание отдела')),
            ],
            options={
                'db_table': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, help_text='Введите имя', max_length=50, null=True, verbose_name='Имя')),
                ('last_name', models.CharField(help_text='Введите имя', max_length=100, verbose_name='Фамилия')),
                ('date_birth', models.DateField(help_text='Введите дату рождения', verbose_name='Дата рождения')),
            ],
            options={
                'db_table': 'Employee',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название команды', max_length=20, verbose_name='Имя команды')),
                ('number', test_django.models.IntegerRangeField(help_text='Введите номер команды', verbose_name='Номер группы')),
            ],
            options={
                'db_table': 'Team',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation', test_django.models.IntegerRangeField(help_text='Введите оценку за проект от 0 до 10', verbose_name='Оценка проекта')),
                ('deadline', models.DateField(help_text='Введите дату сдачи', verbose_name='Срок сдачи')),
                ('chief', models.ForeignKey(help_text='Выберите начальника отдела', on_delete=django.db.models.deletion.CASCADE, to='test_django.chief', verbose_name='Имя')),
                ('employee', models.ForeignKey(help_text='Выберите сотрудника', on_delete=django.db.models.deletion.CASCADE, to='test_django.employee', verbose_name='Сотрудник')),
            ],
            options={
                'db_table': 'Project',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='team',
            field=models.ForeignKey(help_text='Введите номер команды', on_delete=django.db.models.deletion.CASCADE, to='test_django.team', verbose_name='Номер команды'),
        ),
        migrations.AddField(
            model_name='chief',
            name='department',
            field=models.ForeignKey(help_text='Выберите отдел', on_delete=django.db.models.deletion.CASCADE, to='test_django.department', verbose_name='Имя отдела'),
        ),
    ]
