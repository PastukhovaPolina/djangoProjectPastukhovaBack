"""
URL configuration for djangoProjectPastukhova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from test_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info, name='info'), # Просмотр информации после входа
    path('', views.sign_up_log_in), #Начальная страница
    path('cheifView/<int:id_team>/<int:id_user>/addproject/', views.add_project, name='add_project'), # Добавить проект
    path('cheifView/<int:id_team>/<int:id_user>/<int:number_project>/deleteproject/', views.delete_project, name='delete_project'), # Удалить проект

    path('signup_login/', views.sign_up_log_in, name='signup_login'), # Начальная регистрация
    path('register_employee/', views.register_employee, name='register_employee'), # Вторая форма регистрации
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'), # Выход из аккаунта
    path('user_logout', views.logout_user, name='logout_user'),

    path('chiefView/<str:name_office>/', views.show_team_ofOffice, name='employee_ofOffice'), # Переход на просмотр списка команд
    path('chiefView/<str:name_office>/<int:id_team>/', views.show_employeeFromTeam, name='employee_fromTeam'), # Переход на просмотр списка работников команды
    path('chiefView/<int:team_id>/<int:id_user>/', views.show_employee, name='show_employee'), # Открыть карточку работника через работника
    path('asdf/<int:id_team>/<int:id_employee>/', views.employee_info, name='employee_info'), # Открыть карточку работника через через начальника

    #ajax url
    path('ajax/validate_username', views.validate_username, name='validate_username'),
    path('ajax/validate_email', views.validate_email, name='validate_email'),
    path('ajax/check_project_number/<int:id_employee>/', views.check_numberProject, name='check_project_number'),
]
