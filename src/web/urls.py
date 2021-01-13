"""midSINweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
import midsin.web.views

urlpatterns = [
    path('', midsin.web.views.home, name="home"),
    path('oneplate', midsin.web.views.oneplate, name="oneplate"),
    path('batch', midsin.web.views.batch, name="batch"),
    path('csv_template', midsin.web.views.csv_template, name="csv_template"),
    path('download_batchres', midsin.web.views.download_batchres, name="download_batchres"),
]
