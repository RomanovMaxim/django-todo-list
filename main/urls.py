from django.urls import path

from .views import index, addTodo, completeTodo, importantTodo, deleteTodo,\
                   TodoLoginView, TodoLogoutView, ChangeUserInfoView,\
                   TodoPasswordChangeView, RegisterUserView, RegisterDoneView,\
                   user_activate, DeleteUserView

app_name = 'main'

urlpatterns = [
    path('accounts/password/change/', TodoPasswordChangeView.as_view(),
                                      name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/login/', TodoLoginView.as_view(), name='login'),
    path('accounts/logout/', TodoLogoutView.as_view(), name='logout'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('add/', addTodo, name='add'),
    path('complete/<todo_id>', completeTodo, name='complete'),
    path('important/<todo_id>', importantTodo, name='important'),
    path('delete/<todo_id>', deleteTodo, name='delete'),
    path('', index, name='index'),
]
