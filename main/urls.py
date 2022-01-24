import imp
from unicodedata import name
from django.urls import path
from .views import TodoDelete, TodoList, TodoDetail, TodoCreate, TodoUpdate, Login, Register
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',TodoList.as_view(), name ="todos"),
    path('todo/<int:pk>/',TodoDetail.as_view(), name ="todo"),
    path('createTodo/',TodoCreate.as_view(), name ="createTodo"),
    path('updateTodo/<int:pk>/',TodoUpdate.as_view(), name ="updateTodo"),
    path('deleteTodo/<int:pk>/',TodoDelete.as_view(), name ="deleteTodo"),
    path('login/',Login.as_view(), name ="login"),
    path('logout/',LogoutView.as_view(next_page="login"), name ="logout"),
    path('register/',Register.as_view(), name ="register"),
]