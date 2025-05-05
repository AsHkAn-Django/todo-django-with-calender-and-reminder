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
    
    def form_valid(self, form):
        """Duplicate Checker."""
        # we didn't use form.cleaned_data['title'] because it raise an error if there is no value
        category_name = form.cleaned_data.get('title')
        if Category.objects.filter(title__iexact=category_name).exists():
            form.add_error('title', 'This category already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)



class AddTaskView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "myApp/add_task.html"

    def get_success_url(self):
        return reverse_lazy('myApp:category_filter_list', args=[self.object.category.id])
