from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from list.models import Client

User = get_user_model()


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        mail = request.POST.get("mail")
        nom = request.POST.get("username")
        prenom = request.POST.get("username")
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=mail)


        client = Client(nom=nom,
                        prenom=prenom,
                        email=mail)
        client.save()

        login(request, user)
        return redirect('index')
    return render(request, 'accounts/signup.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')

def reset_password(request):
    pass





