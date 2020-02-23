from django.db import models

# Create your models here.
class users(models.Model):
    uid = models.CharField(max_length=50, null=False)
    question = models.CharField(max_length=250, null=False)
    
    def __str__(self):
        return self.uid
