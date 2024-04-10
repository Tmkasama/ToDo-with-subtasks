from django.shortcuts import render, redirect
from .models import Category, SubTask
from django.views import View
from django.views.generic.edit import FormView

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


class TodoListView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            Alldata = Category.objects.filter(user=user)
            context = {"items": Alldata}
            return render(request, self.template_name, context)
        else:
            return redirect('login')


class AddTodoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST['test']
        user = request.user
        Category.objects.create(name=data, user=user)
        return redirect('todoTask')


class DeleteTodoView(LoginRequiredMixin, View):
    def get(self, request, todo_id, *args, **kwargs):
        task = Category.objects.get(pk=todo_id)
        task.delete()
        return redirect('todoTask')


class UpdateTodoView(LoginRequiredMixin, View):
    def post(self, request, todo_id, *args, **kwargs):
        updated_text = request.POST.get('updated_text')
        task = Category.objects.get(pk=todo_id)
        task.name = updated_text
        task.save()
        return redirect('todoTask')


class ViewSubtasksView(LoginRequiredMixin, View):
    template_name = 'subtasks.html'

    def get(self, request, todo_id, *args, **kwargs):
        task = Category.objects.get(pk=todo_id)
        subtasks = task.subtasks.all()
        context = {'task': task, 'subtasks': subtasks}
        return render(request, self.template_name, context)


class AddSubtaskView(LoginRequiredMixin, View):
    def post(self, request, todo_id, *args, **kwargs):
        subtask_name = request.POST.get('subtask_name')
        task = Category.objects.get(pk=todo_id)
        subtask = SubTask.objects.create(name=subtask_name, task=task)
        task.subtasks.add(subtask)
        task.save()
        return redirect('view_subtasks', todo_id=todo_id)


class DeleteSubtaskView(LoginRequiredMixin, View):
    def get(self, request, todo_id, subtask_id, *args, **kwargs):
        subtask = SubTask.objects.get(pk=subtask_id)
        subtask.delete()
        return redirect('view_subtasks', todo_id=todo_id)


class UpdateSubtaskView(LoginRequiredMixin, View):
    def post(self, request, todo_id, subtask_id, *args, **kwargs):
        updated_subtask_name = request.POST.get('updated_subtask')
        subtask = SubTask.objects.get(pk=subtask_id)
        subtask.name = updated_subtask_name
        subtask.save()
        return redirect('view_subtasks', todo_id=todo_id)


class RegisterPageView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todoTask')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPageView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todoTask')
        return super(RegisterPageView, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todoTask')
