from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProjectDB(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    essay = models.TextField()
    price = models.FloatField()
    probability = models.FloatField()
