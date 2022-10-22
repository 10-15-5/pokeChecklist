from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. Welcome to my Pokemon API project")


def home(request):
    context = {"name":"user"}
    return render(request, 'test.html', context)


def about(request):
    return render(request, 'test-about.html')
