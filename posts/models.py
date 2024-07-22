from django.db import models
from django.utils import timezone

class Post(models.Model):
    content = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content