from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
	path('teachers/', include((
	[
        path('', teachers.QuizListView.as_view(), name='quiz_change_list')))),

]
