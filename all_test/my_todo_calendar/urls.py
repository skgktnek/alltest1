from django.urls import path
from . import views

app_name= 'my_todo_calendar'
urlpatterns = [ 
    path('', views.MyCalendarView.as_view(), name='my_calendar'),
    path('event/new/', views.create_event, name='event_new'),
    path('event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),
    path('event/<int:event_id>/details/', views.event_details, name='event-detail'),
    path('event/delete/<int:pk>/', views.EventDelete.as_view(), name='event_delete'),

    
   
] 