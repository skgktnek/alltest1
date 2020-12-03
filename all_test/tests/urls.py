from django.urls import path
from . import views

app_name= 'tests'
urlpatterns = [ 
    path('my_test_calendar/', views.TestCalendarView.as_view(), name='my_test_calendar'),
    path('index/', views.index, name='index'),
    path('<int:test_id>/', views.detail, name='detail'),
    path('<int:test_id>/like/', views.like, name='like'),
    
   
] 