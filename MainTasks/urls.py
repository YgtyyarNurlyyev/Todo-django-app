from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete , CustomLoginView , Register, CheckTask, index, destroy
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='main'),
    path('destroycookie/', destroy, name='cdestroy'),
    path('login/', CustomLoginView.as_view() , name = 'login' ),
    path('logout/', LogoutView.as_view(next_page = 'main'), name = 'logout'),
    path('register/',Register.as_view(),name='register'),
    path('tasks/', TaskList.as_view(), name = 'tasks'),
    path('tasks/check/', CheckTask.as_view(), name='task-check'),
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task' ),
    path('task-create/', TaskCreate.as_view(), name = 'task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name = 'task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view() , name = 'task-delete'),

]