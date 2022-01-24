import imp
from multiprocessing import context
from pyexpat import model
from re import search, template
from statistics import mode
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Todo

class TodoList(LoginRequiredMixin,ListView):
    model = Todo
    context_object_name = 'todos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['todos'] = context['todos'].filter(user = self.request.user)
        context['incomplete_count'] = context['todos'].filter(is_complete = False).count()

        search_input = self.request.GET.get('search') or ''
        if search_input:
            context['todos'] = context['todos'].filter(title__startswith = search_input)
        
        context['search_input'] = search_input
        return context

class TodoDetail(LoginRequiredMixin,DetailView):
    model = Todo
    context_object_name = 'todo'
    template_name = "main/todo.html"

class TodoCreate(LoginRequiredMixin,CreateView):
     model = Todo
     fields = ['title','description','is_complete']
     success_url = reverse_lazy('todos')

     def form_valid(self, form):
         form.instance.user = self.request.user
         return super(TodoCreate,self).form_valid(form)

class TodoUpdate(LoginRequiredMixin,UpdateView):
    model = Todo
    fields = ['title','description','is_complete']
    success_url = reverse_lazy('todos')##redirection

class TodoDelete(LoginRequiredMixin,DeleteView):
    model = Todo
    context_object_name = "todo"
    success_url = reverse_lazy('todos')

class Login(LoginView):
    template_name = "main/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todos')

class Register(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('todos')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect('todos')
        return super(Register, self).get(*args, **kwargs)