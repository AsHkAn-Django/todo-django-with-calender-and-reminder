from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render

from .models import Task, Category
from .forms import TaskForm, CategoryForm, FilterForm



class IndexView(generic.TemplateView):
    template_name = "myApp/index.html"
    
 
      
def filter_list(request):
    tasks = Task.objects.all()
    form = FilterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            category = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            if category:
                tasks = tasks.filter(category_id=category)
            if priority:
                tasks = tasks.filter(priority=priority)
    else:
        form = FilterForm()

    print(tasks)
    return render(request, 'myApp/filter_list.html', {'tasks': tasks, 'form': form})



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
