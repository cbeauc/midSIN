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
    #path('admin/', admin.site.urls),
    path('', midsin.web.views.index, name="index"),
    path('oneplate', midsin.web.views.oneplate, name="oneplate"),
    path('batch', midsin.web.views.batch, name="batch"),
    path('test', midsin.web.views.test, name="test"),
]
