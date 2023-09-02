from django.db import models

from django_time_for_a_boolean.fields import BooleanDateField
from django_time_for_a_boolean.fields import BooleanDateTimeField


# Create your models here.
class Example(models.Model):
    deleted = BooleanDateTimeField()
    ended = BooleanDateField()
