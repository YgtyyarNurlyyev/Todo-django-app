from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    tittle = models.CharField(max_length=200, null=True, blank=True )
    complete = models.BooleanField(default=False)
    DoTime = models.TimeField()

    def __str__(self):
        return self.tittle

    