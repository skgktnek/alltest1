from django.urls import path

from . import views
app_name='test_info'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:test_id>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:test_id>/edit/', views.edit, name='edit'),
    path('<int:test_id>/update/', views.update, name='update'),
    path('<int:test_id>/delete/', views.delete, name='delete'),
    path('<int:test_id>/like/', views.like, name='like'),
]
