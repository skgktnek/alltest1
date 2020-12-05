
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from tests.models import Test

# Create your views here.
def index(request):
    tests = Test.objects.all()
    context = {
        'tests' : tests
    }
    return render(request, 'mainpage/index.html', context)

# def login(request):
#     return render(request, 'mainpage/login.html')

# def calendar(request):
#     return render(request, 'mainpage/calendar.html')