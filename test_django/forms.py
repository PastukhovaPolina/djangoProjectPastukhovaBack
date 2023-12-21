from .models import Project
from django.forms import ModelForm, TextInput, DateInput
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput


# class ProjectForm(ModelForm):
#     class Meta:
#         model = Project
#         fields = ['employee', 'office', 'evaluation', 'deadline', 'number']
#
#         widgets = {
#             'employee': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Работник'
#             }),
#             'office': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Офис'
#             }),
#             'evaluation': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Рейтинг'
#             }),
#             'deadline': DateInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Дедлайн'
#             }),
#             'number': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Номер проекта'
#             }),
#         }


class ProjectForm(forms.Form):
    number = forms.IntegerField(help_text="Введите номер проекта", min_value=1, max_value=12)
    evaluation = forms.IntegerField(help_text="Введите оценку для проекта", min_value=1, max_value=10)
    deadline = forms.DateField(help_text="Выберите дату сдачи проекта", widget=DatePickerInput())


class EmployeeForm(forms.Form):
    name = forms.CharField(help_text="Введите имя")
    surname = forms.CharField(help_text="Введите фамилию")
    birth_date = forms.DateField(help_text="Выберите дату рождения", widget=DatePickerInput())
    team = forms.IntegerField(help_text="Введите номер команды")
