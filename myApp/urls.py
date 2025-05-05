from django.urls import path
from . import views

app_name = 'myApp'
urlpatterns = [
  
	path('filter/', views.filter_list, name='filter_list'),
	path('category_list/tasks/', views.AllTasksView.as_view(), name='all_tasks'),
	path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
	path('add_task/', views.AddTaskView.as_view(), name='add_task'),
	path('', views.IndexView.as_view(), name='home'),
]
