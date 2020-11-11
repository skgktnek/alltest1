
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'mainpage/index.html')

def login(request):
    return render(request, 'mainpage/login.html')

def calendar(request):
    return render(request, 'mainpage/calendar.html')