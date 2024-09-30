from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')

def Services(request):
    return render(request, 'main/Services.html')
