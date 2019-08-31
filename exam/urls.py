from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('students/', include(([
    ], 'classroom'), namespace='students')),


]
