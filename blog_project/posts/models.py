from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    content = models.TextField()

    def __str__(self):
        return self.title
