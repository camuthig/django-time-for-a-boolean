from django.db import models

from django_time_for_a_boolean import BooleanDateField
from django_time_for_a_boolean import BooleanDateTimeField


class Example(models.Model):
    datetime_field = BooleanDateTimeField()
    datetime_column_field = BooleanDateTimeField(db_column="datetime_column_field_by")

    date_field = BooleanDateField()
    date_column_field = BooleanDateField(db_column="date_column_field_after")

    default_datetime_field = BooleanDateTimeField(default=True)
    default_date_field = BooleanDateField(default=True)
