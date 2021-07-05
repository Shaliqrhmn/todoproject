from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Task
from .froms import TaskForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView


# Create your views here.
def index(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date' '')
        task = Task(task_name=task_name, priority=priority, date=date)
        task.save()

    items = Task.objects.all()
    context = {'items': items}

    return render(request, 'index.html', context)


class TaskListView(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'items'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'items'


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'edit.html'
    context_object_name = 'items'
    fields = ('task_name', 'priority', 'date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'items'

    def get_success_url(self):
        return reverse_lazy('cbvhome', kwargs={'pk': self.object.id})


def delete(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')


def update(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'update.html', {'form': form, 'task': task})
