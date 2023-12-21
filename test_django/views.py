import hashlib
import os
from pathlib import Path

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect

from test_django.forms import ProjectForm, EmployeeForm
from test_django.models import Employee, Project, Chief, Office, Team

BASE_DIR = Path(__file__).resolve().parent.parent


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/signup_login')


# Если начальник, то переходим на выбор офиса.
# Если работник, то смотрим карточку работника.
def show_info(request):
    user = request.user

    if user.is_authenticated:
        if user.groups.filter(name="Начальники").exists():
            chief = Chief.objects.get(id_user_id=user.id)
            office = list(Office.objects.filter(chief_id=chief.id))
            return render(request, 'chiefView.html', {"office": office})
        else:
            employee = Employee.objects.get(id_user_id=user.id)
            projects = Project.objects.filter(employee=employee.id)
            projects = list(projects)
            return render(request,
                          'employeeInfo.html',
                          {"employee": employee,
                           "projects": projects,
                           })
    else:
        return redirect("/signup_login")

# Открыть карточку работника через через начальника
def employee_info(request, id_team, id_employee):
    return render(request, 'chiefEmployeeInfo.html',
                  {"employee": Employee.objects.get(id=id_employee),
                   "projects": Project.objects.filter(employee_id=id_employee),
                   "id_team": id_team
                   })


# Открыть карточку работника через работника
def show_employee(request, id_team, id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Начальники").exists():
        employee = Employee.objects.get(id_user_id=id_user)
        projects = Project.objects.filter(employee=employee.id)
        projects = list(projects)
        return render(request,
                      'employeeInfo.html',
                      {"employee": employee,
                       "link_img": hashlib.md5(
                           User.objects.get(id=employee.id_user_id).email.encode('utf-8')).hexdigest(),
                       "projects": projects,
                       "team_id": id_team,
                       })
    else:
        return render(request, 'notAccess.html')


#
# def show_chief_employee(request, id_team, id_user, name_office):
#     user = request.user
#     if user.is_authenticated and user.groups.filter(name="Начальники").exists():
#         employee = Employee.objects.get(id_user_id=id_user)
#         projects = Project.objects.filter(employee=employee.id)
#         projects = list(projects)
#         return render(request,
#                       'chiefEmployeeInfo.html',
#                       {"employee": employee,
#                        "link_img": hashlib.md5(
#                            User.objects.get(id=employee.id_user_id).email.encode('utf-8')).hexdigest(),
#                        "projects": projects,
#                        "id_team": id_team,
#                        "name_office": name_office,
#                        })
#     else:
#         return render(request, 'notAccess.html')


# Начальная регистрация
def sign_up_log_in(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info")
        else:
            return render(request, 'index.html')

    else:
        print(request.body)
        if (request.POST.get("email") != None):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
                return render(request, 'employeeInfo.html', {'employee': Employee.objects.get(id_user_id=user.id),
                                                             'projects': Project.objects.filter(
                                                                 employee_id=Employee.objects.get(
                                                                     id_user_id=user.id).id),
                                                             'id_team': Employee.objects.get(
                                                                 id_user_id=user.id).team_id})
            except Exception:
                print("Not correct email or pass")
                return redirect("/signup_login/")
        else:
            email = request.POST.get("create_email")
            username = request.POST.get("create_user_name")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            Employee.objects.create(id_user_id=user.id)
            return redirect("/register_employee")


# Вторая форма регистрации
def register_employee(request):
    if request.method == 'GET':
        form = EmployeeForm()
        return render(request, 'registerEmployee.html', {'form': form})
    else:
        form = EmployeeForm(request.POST)
        if form.is_valid():
            Employee.objects.filter(id_user_id=request.user).update(first_name=form.cleaned_data['name'],
                                                                    last_name=form.cleaned_data['surname'],
                                                                    date_birth=form.cleaned_data['birth_date'],
                                                                    team_id=form.cleaned_data['team'])
            return redirect('/info')
        else:
            print("asdfasdfasdf")


# Добавить проект
def add_project(request, id_team, id_user):
    if request.method == "GET":
        projectForm = ProjectForm()
        return render(request, "templateForm.html",
                      {"form": projectForm, "id_employee": Employee.objects.get(id_user=id_user).id})
    else:
        projectform = ProjectForm(request.POST)
        if projectform.is_valid():
            obj = Project()
            obj.employee = Employee.objects.get(id_user_id=id_user)
            obj.number = projectform.cleaned_data['number']
            obj.evaluation = projectform.cleaned_data['evaluation']
            obj.deadline = projectform.cleaned_data['deadline']
            obj.save()
            if User.objects.get(id=id_user).groups.filter(name="Начальники").exists():
                return redirect(f"/chiefView/{id_team}/{id_user}")
            else:
                return render(request, 'chiefEmployeeInfo.html', {'employee': Employee.objects.get(id_user_id=id_user),
                                                             'projects': Project.objects.filter(
                                                                 employee_id=Employee.objects.get(
                                                                     id_user_id=id_user).id),
                                                             'id_team': Employee.objects.get(
                                                                 id_user_id=id_user).team_id})
        else:
            return redirect("/")


# Удалить проект
def delete_project(request, id_team, id_user, number_project):
    employee_id = Employee.objects.get(id_user_id=id_user).id
    project = Project.objects.filter(number=number_project, employee_id=employee_id).delete()
    if User.objects.get(id=id_user).groups.filter(name="Начальники").exists():
        return redirect(f"/chiefView/{id_team}/{id_user}")
    else:
        return render(request, 'chiefEmployeeInfo.html', {'employee': Employee.objects.get(id_user_id=id_user),
                                                     'projects': Project.objects.filter(
                                                         employee_id=Employee.objects.get(id_user_id=id_user).id),
                                                     'id_team': id_team
                                                     })


# Переход на просмотр списка команд
def show_team_ofOffice(request, name_office):
    office = Office.objects.get(name_office=name_office)
    team = office.team.filter(office=office.name_office)
    return render(request, 'chiefViewTeam.html', {"team": team, "name_office": name_office})


# Переход на просмотр списка работников команды
def show_employeeFromTeam(request, name_office, id_team):
    employees = Employee.objects.filter(team_id=id_team)
    employeeAllProjects = []
    employeeLastProjects = []
    for employee in employees:
        employeeProjects = Project.objects.filter(employee_id=employee.id)
        if employeeProjects:
            # project_status = employee.project_set.values_list('project_status', flat=True)
            averageEvaluation = employeeProjects.aggregate(Avg("evaluation"))['evaluation__avg']
            employeeAllProjects.append(averageEvaluation)
            employeeLastProjects.append(max(map(lambda x: x.number, employeeProjects)))
        else:
            employeeAllProjects.append(0)
            employeeLastProjects.append(0)
    employees = zip(employees, employeeAllProjects, employeeLastProjects)
    print(id_team)
    return render(request, 'chiefViewEmployee.html',
                  {"employees": employees, "id_team": id_team})


# AJAX view
def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def validate_email(request):
    email = request.GET.get('create_email', None)
    response = {
        'taken': User.objects.filter(email__exact=email).exists()
    }
    return JsonResponse(response)


def check_numberProject(request, id_employee):
    number = int(request.GET.get('number', None))
    if (number == ""):
        number = 0
    response = {
        'exist': Project.objects.filter(number=number, employee_id=id_employee).exists()
    }
    return JsonResponse(response)
# версия на 16.12
# def show_info(request, name_office, id_team, id_user):
#     user = request.user
#
#     if user.is_authenticated:
#         if user.groups.filter(name="Начальники").exists():
#             chief = Chief.objects.get(id_user_id=user.id)
#             office = list(Office.objects.filter(chief_id=chief.id))
#             return render(request, 'chiefView.html', {"office": office})
#         else:
#             employee = Employee.objects.get(id_user_id=user.id)
#             projects = list(Project.objects.filter(employee=employee.id))
#             return render(request,
#                           'employeeInfo.html',
#                           {"employee": employee,
#                            "link_img": hashlib.md5(user.email.encode('utf-8')).hexdigest(),
#                            "projects": projects,
#                            "name_office": name_office,
#                            "id_team": id_team
#
#                            })
#     else:
#         return redirect("/")
#
# def employee_info(request, id_team, id_employee):
#     return render(request, 'employeeInfo.html',
#                           {"employee": Employee.objects.get(id=id_employee),
#                            "projects": Project.objects.filter(employee_id=id_employee),
#                            "id_team": id_team
#                            })
# def show_employee(request, name_office, id_team, id_user):
#     user = request.user
#     if user.is_authenticated and user.groups.filter(name="Начальники").exists():
#         employee = Employee.objects.get(id_user_id=id_user)
#         projects = Project.objects.filter(employee=employee.id)
#         projects = list(projects)
#         return render(request,
#                       'employeeInfo.html',
#                       {"employee": employee,
#                        "link_img": hashlib.md5(
#                            User.objects.get(id=employee.id_user_id).email.encode('utf-8')).hexdigest(),
#                        "projects": projects,
#                        "name_office": name_office,
#                        "id_team": id_team,
#                        })
#     else:
#         return render(request, 'notAccess.html')
#
#
# def sign_up_log_in(request):
#     if request.method == "GET":
#         cur_user = request.user
#         if cur_user.is_authenticated:
#             return redirect("/info")
#         else:
#             return render(request, 'index.html')
#
#     else:
#         print(request.body)
#         if (request.POST.get("email") != None):
#             email = request.POST.get("email")
#             password = request.POST.get("password")
#             username = User.objects.get(email=email).username
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             if user.groups.filter(name="Начальники").exists():
#                 return redirect(f"/info/g/1/{user.id}")
#             employee = Employee.objects.get(id_user_id=user.id)
#             id_team = employee.team_id
#             name_office = Office.objects.get(team=id_team).name_office
#             return redirect(f"/info/{name_office}/{id_team}/{user.id}")
#            # try:
#            #      login(request, user)
#            #      return redirect("/info")
#            #  except Exception:
#            #      print("Not correct email or pass")
#            #      return redirect("")
#         else:
#             email = request.POST.get("create_email")
#             username = request.POST.get("create_user_name")
#             password = request.POST.get("create_password")
#             user = User.objects.create_user(email=email, username=username, password=password)
#             login(request, user)
#             return redirect("/info")
#
#
# def add_project(request, name_office, id_team, id_user):
#     if request.method == "GET":
#         projectForm = ProjectForm()
#         return render(request, "templateForm.html", {"form": projectForm, "name_office": name_office, "id_employee": Employee.objects.get(id_user=id_user).id})
#     else:
#         projectform = ProjectForm(request.POST)
#         if projectform.is_valid():
#             obj = Project()
#             obj.employee = Employee.objects.get(id_user_id=id_user)
#             obj.number = projectform.cleaned_data['number']
#             obj.evaluation = projectform.cleaned_data['evaluation']
#             obj.deadline = projectform.cleaned_data['deadline']
#             obj.save()
#             return redirect("show_employee", name_office=name_office, id_team=id_team, id_user=id_user)
#             #return redirect(f"/info/{name_office}/{id_team}/{id_user}")
#         else:
#             return redirect("/")
#
#
# def delete_project(request, name_office, id_team, id_user, number_project):
#     employee_id = Employee.objects.get(id_user_id=id_user).id
#     project = Project.objects.filter(number=number_project, employee_id=employee_id).delete()
#     if User.objects.get(id=id_user).groups.filter(name="Начальники").exists():
#         return redirect(f"/chiefView/{name_office}/{id_team}/{id_user}")
#     #return redirect(f"/show_employee/{name_office}/{id_team}/{id_user}")
#     return redirect("show_employee", name_office=name_office, id_team=id_team, id_user=id_user)
#
# def show_team_ofOffice(request, name_office):
#     office = Office.objects.get(name_office=name_office)
#     team = office.team.filter(office=office.name_office)
#     return render(request, 'chiefViewTeam.html', {"team": team, "name_office": name_office})
#
#
# def show_employeeFromTeam(request, id_team, name_office):
#     employees = Employee.objects.filter(team=Team.objects.get(id=id_team))
#     employeeAllProjects = []
#     employeeLastProjects = []
#     for employee in employees:
#         employeeProjects = Project.objects.filter(employee_id=employee.id)
#         averageEvaluation = employeeProjects.aggregate(Avg("evaluation"))['evaluation__avg']
#         employeeAllProjects.append(averageEvaluation)
#         employeeLastProjects.append(max(map(lambda x: x.number, employeeProjects)))
#     employees = zip(employees, employeeAllProjects, employeeLastProjects)
#     return render(request, 'chiefViewEmployee.html',
#                   {"employees": employees, "name_office": name_office, "id_team": id_team})
#
#
# # AJAX view
# def validate_username(request):
#     username = request.GET.get('create_user_name', None)
#     response = {
#         'taken': User.objects.filter(username__exact=username).exists()
#     }
#     return JsonResponse(response)
#
# def validate_email(request):
#     email = request.GET.get('create_email', None)
#     response = {
#         'taken': User.objects.filter(email__exact=email).exists()
#     }
#     return JsonResponse(response)
#
# def check_numberProject(request, name_office, id_employee):
#     number = int(request.GET.get('number', None))
#     if (number == ""):
#         number = 0
#     office_obj = Office.objects.get(name_office=name_office)
#     response = {
#         'exist': Project.objects.filter(number=number, office=office_obj, employee_id=id_employee).exists()
#     }
#     return JsonResponse(response)
