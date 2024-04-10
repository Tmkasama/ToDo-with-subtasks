from django.urls import path
from .views import *

urlpatterns = [
    path('', TodoListView.as_view(), name='todoTask'),
    path('add/', AddTodoView.as_view(), name='add'),
    path('delete/<int:todo_id>/', DeleteTodoView.as_view(), name='delete'),
    path('update/<int:todo_id>/', UpdateTodoView.as_view(), name='update'),

    path('subtasks/<int:todo_id>/', ViewSubtasksView.as_view(), name='view_subtasks'),
    path('subtasks/add/<int:todo_id>/', AddSubtaskView.as_view(), name='subtaskAdd'),
    path('subtasks/<int:todo_id>/delete/<int:subtask_id>/', DeleteSubtaskView.as_view(), name='subtaskDelete'),
    path('subtasks/update/<int:todo_id>/<int:subtask_id>/', UpdateSubtaskView.as_view(), name='subtaskUpdate'),
    
    path('register/', RegisterPageView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
