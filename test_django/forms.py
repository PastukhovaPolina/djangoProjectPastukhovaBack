from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput


class ProjectForm(forms.Form):
    number = forms.IntegerField(help_text="Введите номер проекта", min_value=1, max_value=12)
    evaluation = forms.IntegerField(help_text="Введите оценку для проекта", min_value=1, max_value=10)
    deadline = forms.DateField(help_text="Выберите дату сдачи проекта", widget=DatePickerInput())


class EmployeeForm(forms.Form):
    name = forms.CharField(help_text="Введите имя")
    surname = forms.CharField(help_text="Введите фамилию")
    birth_date = forms.DateField(help_text="Выберите дату рождения", widget=DatePickerInput())
    team = forms.IntegerField(help_text="Введите номер команды")
