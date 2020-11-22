from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Test
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
# render: 어떤 템플릿을 그릴 것인지

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def index(request):
    tests = Test.objects.all()

    context = {'tests': tests}

    return render(request, 'test_info/index.html', context)

def detail(request, test_id):
    test = Test.objects.get(id=test_id)
    context = { 'test' : test }
    return render(request, 'test_info/detail.html', context)

@login_required
def new(request): 
    return render(request, 'test_info/new.html')    

@login_required
def create(request):
#    if not request.user.is_authenticated:
#        return redirect('accounts:login') 
# login_required 기능을 사용하지 않는다면 위 두줄 코드를 사용해야 함.

    user = request.user
    body = request.POST['body']

    image = None
    if 'image' in request.FILES:
        image = request.FILES['image']

    test = Test(user=user, body=body, image=image, created_at=timezone.now())
    test.save()

    return redirect('test_info:detail', test_id=test.id)    

@login_required
def edit(request, test_id):
    try:
        test = Test.objects.get(id=test_id, user=request.user)
    except Test.DoesNotExist:
        return redirect('test_info:index')

    context = { 'test' : test }
    return render(request, 'test_info/edit.html', context)   

@login_required
def update(request, test_id):
    try:
        Test = Test.objects.get(id=test_id, user=request.user)
    except Test.DoesNotExist:
        return redirect('test_info:index')

    test.body = request.POST['body']

    if 'image' in request.FILES:
        test.image = request.FILES['image']

    test.save()

    return redirect('test_info:detail', test_id=test.id)        

@login_required
def delete(request, test_id):
    try:
        test = Test.objects.get(id=test_id, user=request.user)
    except Test.DoesNotExist:
        return redirect('test_info:index')
    
    test.delete()

    return redirect('test_info:index')   

@login_required
def like(request, test_id):

    if request.method == 'POST':
        try:
            test = Test.objects.get(id=test_id)

            if request.user in test.liked_users.all():
                test.liked_users.remove(request.user)
            else:
                test.liked_users.add(request.user)

            return redirect('test_info:detail', test_id=test.id)

        except Test.DoesNotExist:
            pass

    return redirect('test_info:index')