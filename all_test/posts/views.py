from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'posts': [
            {'author': '_alltest', 'body': 'sample post 1'},
            {'author': '_alltest', 'body': 'sample post 2'},
            {'author': '_alltest', 'body': 'sample post 3    '},
        ]
    }
    return render(request, 'posts/index.html', context)