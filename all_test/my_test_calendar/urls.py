from django.urls import path
from . import views

app_name= 'my_test_calendar'
urlpatterns = [ 
    path('index', views.index, name='index'),
    path('', views.TestCalendarView.as_view(), name='test_calendar'),
    # path('event/new/', views.create_event, name='event_new'),
    # path('event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    # path('event/<int:event_id>/details/', views.event_details, name='event-detail'),
    # path('event/delete/<int:pk>/', views.EventDelete.as_view(), name='event_delete'),
    # path('my_today/<int:year>/<int:month>/<int:day>', views.my_today ,name='my_today')
    
   
] 