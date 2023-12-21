from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Department(models.Model):
    name = models.CharField(max_length=150, primary_key=True, verbose_name="Имя отдела",
                            help_text="Введите название отдела", null=False, blank=False)
    description = models.TextField(verbose_name="описание отдела")

    def __str__(self):
        return "Отдел: " + self.name

    class Meta:
        db_table = "Department"


class Team(models.Model):
    name = models.CharField(max_length=20, verbose_name="Имя команды",
                            help_text="Введите название команды", null=False, blank=False)
    number = IntegerRangeField(min_value=1, max_value=5, verbose_name="Номер группы",
                               help_text="Введите номер команды", null=False, blank=False)

    def __str__(self):
        return "Команда: " + self.name

    class Meta:
        db_table = "Team"


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя",
                                  help_text="Введите имя", null=True, blank=False)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия",
                                 help_text="Введите имя", null=False, blank=False)
    date_birth = models.DateField(verbose_name="Дата рождения",
                                  help_text="Введите дату рождения", null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Имя команды",
                             help_text="Введите название команды", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Сотрудник: " + self.first_name + " " + self.last_name + " " + self.team.__str__()

    class Meta:
        db_table = "Employee"


class Chief(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя",
                                  help_text="Введите имя", null=False, blank=False)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия",
                                 help_text="Введите фамилию", null=False, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Имя отдела",
                                   help_text="Выберите отдел", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Начальник: " + self.first_name + " " + self.last_name + " " + self.department.__str__()

    class Meta:
        db_table = "Chief"


class Office (models.Model):
    name_office = models.CharField(max_length=100, verbose_name="Название офиса",
                                    help_text="Введите название офиса", null=False, blank=False, primary_key=True)

    chief = models.ForeignKey(Chief, on_delete=models.CASCADE, verbose_name="Начальник",
                              help_text="Выберите начальника отдела", null=False, blank=False)
    team = models.ManyToManyField(Team)


class Project(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник",
                                 help_text="Выберите сотрудника", null=False, blank=False)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name="Офис",
                               help_text="Введите название офиса", null=False, blank=False, default="Золотое яблоко",
                               db_column="office")
    evaluation = IntegerRangeField(min_value=0, max_value=10, verbose_name="Оценка проекта",
                                   help_text="Введите оценку за проект от 0 до 10", null=False, blank=False)
    deadline = models.DateField(verbose_name="Срок сдачи",
                                help_text="Введите дату сдачи", null=False, blank=False)
    number = IntegerRangeField(verbose_name="Номер проекта", min_value=1, default=1,
                              help_text="Введите номер проекта", null=False, blank=False)

    def __str__(self):
        return "Сдал: " + self.employee.__str__() + " Оценка: " + str(self.evaluation)

    class Meta:
        db_table = "Project"
