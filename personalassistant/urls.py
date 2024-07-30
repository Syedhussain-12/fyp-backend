"""
URL configuration for personalassistant project.

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
from django.urls import path
from personal_assistant_backend import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.user),
    path('assistant/', views.assistant),
    path('test/', views.test),
    path('calendar/', views.calendar),
    path('combineAgent/', views.combineAgent),
    path('insertChat/', views.insert_and_fetch_chats),
    path('getChat/', views.get_chat_data),
    path('filterChat/', views.fetch_chats_by_date_and_email),
    

]

urlpatterns = format_suffix_patterns(urlpatterns)
