"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
# from django.urls import include, re_path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('hot/', views.hot_questions, name='hot'),
    path('settings/', views.form_with_settings, name='settings'),
    path('tag/<slug:tag>/', views.question_by_tag, name='by_tag'),
    path('question/<int:num_quest>', views.one_question_page, name='one_question'),
    path('login/', views.autorisation, name='login'),
    path('logout/', views.logout, name='logout'),
    path('singup/', views.registration, name='sing_up'),
    path('ask/', views.add_question, name='ask'),
]
