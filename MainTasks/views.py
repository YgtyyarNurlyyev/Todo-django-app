from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json


def index(request):
    current_name = ''
    response = render(request, 'MainTasks/main.html', {
        'current_name': current_name,
    })
    if request.method == 'GET':
        if 'name' in request.COOKIES:
            current_name = request.COOKIES['name']
            response = render(request, 'MainTasks/main.html', {
                'current_name': current_name,
            })
    elif request.method == 'POST':
        current_name = request.POST.get('name')
        response = render(request, 'MainTasks/main.html', {
            'current_name': current_name,
        })
        response.set_cookie('name', current_name)
    return response


def destroy(request):
    if 'name' in request.COOKIES:
        currentname = request.COOKIES['name']
        response = render(request, 'MainTasks/destroy.html', {
            'current_name': currentname,
        })
    else:
        response = render(request, 'MainTasks/destroy.html', )
    if 'name' in request.COOKIES:
        response.delete_cookie('name')
    return response


class CustomLoginView(LoginView):
    template_name = 'MainTasks/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class Register(FormView):
    template_name = 'MainTasks/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)


class TaskList(LoginRequiredMixin, ListView):
    model = task
    context_object_name = 'tasks'
    ordering = 'tittle'
    paginate_by = 3

    def get_queryset(self):
        self.order = self.request.GET.get('order', 'asc')
        selected_ordering = self.request.GET.get('ordering', 'tittle')
        self.selected_orderingforpage = selected_ordering
        if self.order == "desc":
            selected_ordering = "-" + selected_ordering
        filter_val = self.request.GET.get('NameFilter', '')
        CheckFiltering = self.request.GET.get('CheckFilter', '')
        startTimer = self.request.GET.get('startTime', '00:00:00')
        endTimer = self.request.GET.get('endTime', '23:59:59')

        new_context = task.objects.filter(
            tittle__icontains=filter_val,
            DoTime__gte=startTimer,
            DoTime__lte=endTimer,
            user=self.request.user,
        ).order_by(selected_ordering)

        if CheckFiltering == 'on':
            new_context = new_context.filter(
                complete=False,
            )

        return new_context

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['order'] = self.order
            context['ordering'] = self.selected_orderingforpage
            context['filter_val'] = self.request.GET.get('NameFilter', '')
            context['CheckFiltering'] = self.request.GET.get('CheckFilter', '')
            context['startTimer'] = self.request.GET.get('startTime', '00:00:00')
            context['endTimer'] = self.request.GET.get('endTime', '23:59:59')
            return context
        except Http404:
            self.kwargs['page'] = 1
            context = super().get_context_data(**kwargs)
            context['order'] = self.order
            context['ordering'] = self.selected_orderingforpage
            context['filter_val'] = self.request.GET.get('NameFilter', '')
            context['CheckFiltering'] = self.request.GET.get('CheckFilter', '')
            context['startTimer'] = self.request.GET.get('startTime', '00:00:00')
            context['endTimer'] = self.request.GET.get('endTime', '23:59:59')
            return context


class CheckTask(View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        task_id = body.get('task')
        todo = get_object_or_404(task, id=task_id)
        if todo.complete:
            todo.complete = False
        else:
            todo.complete = True
        todo.save()
        return HttpResponse('Success')


class TaskDetail(LoginRequiredMixin, DetailView):
    model = task
    context_object_name = 'task'
    template_name = 'MainTasks/task.html'


class TaskCreate(CreateView):
    model = task
    fields = ['tittle', 'complete', 'DoTime']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = task
    fields = ['tittle', 'complete', 'DoTime']
    success_url = reverse_lazy('tasks')
    template_name = 'MainTasks/task_update.html'


class TaskDelete(DeleteView):
    model = task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
