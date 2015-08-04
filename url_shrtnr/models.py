from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=2083)
    slug = models.CharField(max_length=2083)
    views = models.IntegerField(default=0)
