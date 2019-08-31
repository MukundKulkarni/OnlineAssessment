from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('students/', include(([
            path('', views.QuizListView.as_view(), name='quiz_list'),
            path('interests/', views.StudentInterestsView.as_view(), name='student_interests'),

    ], 'classroom'), namespace='students')),


]
