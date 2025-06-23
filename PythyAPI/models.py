from django.db import models

# Create your models here.
class users(models.Model):
    uid = models.CharField(max_length=50, null=False)
    question = models.CharField(max_length=250, null=True)#8
    state = models.CharField(max_length=10, null=False)#10
    created_time = models.DateTimeField(auto_now=True)#12
    
    def __str__(self):
        return self.uid

class teamUp(models.Model):#12
    bid = models.CharField(max_length=50, default='0', null=False)
    place = models.CharField(max_length=30, null=False)
    amount = models.CharField(max_length=5, null=False)
    timein = models.CharField(max_length=20, null=False)
    
    def __str__(self):
        return str(self.id)
