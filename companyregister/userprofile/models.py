import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Register(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    limit = models.IntegerField()

    def __str__(self):
        return self.name


class APILimits(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    registerName = models.ForeignKey(to=Register, on_delete=models.SET_NULL, null=True)
    limit = models.IntegerField()
    resetDate = models.DateField(default=now)
    apiKey = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.owner} ({self.registerName})"

    class Meta:
        verbose_name_plural = 'API Limits'




