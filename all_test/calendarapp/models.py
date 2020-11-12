from django.db import models

class Event(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

        
