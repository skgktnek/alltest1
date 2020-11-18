from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class MyEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    objects = models.Manager()
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('my_todo_calendar:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('my_todo_calendar:event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
