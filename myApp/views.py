from django.urls import reverse_lazy
from django.views import generic
from .models import Task, Category
from .forms import TaskForm, CategoryForm, FilterForm



class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"
    
    

class CategoryFilterListView(generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = "myApp/category_filter_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['category'] = Category.objects.get(id=category_id)
        return context
      


class AllTasksView(generic.ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "myApp/all_tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = FilterForm
        return context

    

class AddCategoryView(generic.CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('myApp:all_tasks')
    template_name = "myApp/add_category.html"



class AddTaskView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "myApp/add_task.html"

    def get_success_url(self):
        return reverse_lazy('myApp:category_filter_list', args=[self.object.category.id])
