"""
URL configuration for score_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from score_table.views import frontpage,post_detail,score_table,index,save_ranking

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",frontpage, name="frontpage"),
    path("score_table/",score_table,name="score_table"),
    path('index/', index, name='index'),
    path('save-ranking/', save_ranking, name='save_ranking'),
    path("<slug:slug>/",post_detail,name="post_detail"),
]
