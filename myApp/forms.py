from django import forms
from .models import Task, Category

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = '__all__'


class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['category', 'title', 'description', 'deadline']
    widgets = {
      'deadline': forms.DateInput(attrs={'type': 'date'}),
    }
    