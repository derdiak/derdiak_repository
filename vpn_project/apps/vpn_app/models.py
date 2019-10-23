from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=30)
    quota = models.DecimalField(max_digits=5, decimal_places=2) # или integer, если в целых терабайтах

    def __str__(self):
        return self.name

    @property
    def users(self):
        return self.user_set.all()

    class Meta:
        verbose_name_plural = "Companies"

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def transfers(self):
        return self.transfer_set.all()

class Transfer(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    datetime = models.DateTimeField(default=timezone.now)
    resource = models.URLField()
    transferred = models.BigIntegerField()
