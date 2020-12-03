from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError


class Test(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=40, null=False)
    test_round = models.IntegerField(default=0)
    register_day_start = models.DateField()
    register_day_end = models.DateField()
    test_day = models.DateTimeField()
    results_day = models.DateTimeField()
    test_fee = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    detail = models.CharField(max_length=200, null=True)
    liked_users = models.ManyToManyField(User, through='Mytests')

 

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('my_todo_calendar:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('my_todo_calendar:event-detail', args=(self.id,))
      
        return f'<a href="{url}"> {self.title} </a>'

class Mytests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)




