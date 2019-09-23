from django.shortcuts import render, redirect
from . models import TitleData
from django.http import HttpResponse
from .forms import UserForm, LoginForm, TagForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
def home(request):
    return render(request, 'notice/home.html')


def email(request):
    context = {
        'notice_list': TitleData.objects.all(),
    }
    return render(request, 'notice/email.html', context)

def empty(request):
    return render(request, 'notice/empty.html')


def email_control(request):
    return render(request, 'notice/email_service_control.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('email')
    else:
        form = UserForm()
        return render(request, 'notice/adduser.html', {'form': form})
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('control')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'notice/login.html', {'form': form})
def addTag(request):
  if request.method == "POST":
      #저장
      form = TagForm(request.POST)
      if form.is_valid():
          tag = form.save(commit = False)
          tag.account = User.objects.get(username = request.user.get_username())
          tag.save()
          return redirect('home')