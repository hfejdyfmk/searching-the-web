import datetime

from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.category_name

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Work(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    work_name = models.CharField(max_length=200)
    work_fname = models.CharField(max_length=50, default="") # django provide FileField, FilePathField, TextField # ref: https://docs.djangoproject.com/en/4.0/ref/models/fields/
    # votes = models.IntegerField(default=0)

    def __str__(self):
        return self.work_name

