from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy

from .models import ToDo
from .forms import TodoForm

def index(request):
    if request.user.is_authenticated:
        todos = ToDo.objects.filter(author=request.user.pk)
        form = TodoForm(initial={'author': request.user.pk})
        context = {'todos': todos, 'form': form,}
        return render(request, 'main/index.html', context)
    else:
        return render(request, 'main/index.html')


from django.contrib.auth.decorators import login_required

@login_required
def addTodo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
        return redirect('main:index')

def completeTodo(request, todo_id):
    todo = ToDo.objects.get(pk=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect('main:index')

def importantTodo(request, todo_id):
    todo = ToDo.objects.get(pk=todo_id)
    todo.is_important = not todo.is_important
    todo.save()
    return redirect('main:index')

def deleteTodo(request, todo_id):
    ToDo.objects.get(pk=todo_id).delete()
    return redirect('main:index')


from django.contrib.auth.views import LoginView

class TodoLoginView(LoginView):
    template_name = 'main/login.html'


from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

class TodoLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import AdvUser
from .forms import ChangeUserInfoForm

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Личные данные пользователя изменены'

    # Получение ключа пользователя
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    # Извлечение записи с данными пользователя
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


from django.contrib.auth.views import PasswordChangeView

class TodoPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


from django.views.generic.edit import CreateView
from .forms import RegisterUserForm

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


from django.views.generic.base import TemplateView

class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


from django.core.signing import BadSignature
from .utilities import signer

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    # Получение ключа пользователя
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    # Выход перед удалением пользователя и вывод сообщения об удалении
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    # Отыскание записи пользователя по найденному ключу в методе dispatch()
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
