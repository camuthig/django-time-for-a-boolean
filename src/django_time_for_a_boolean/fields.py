from datetime import datetime
from typing import Callable

from django.db import models
from django.db.models import Lookup
from django.db.models.query_utils import DeferredAttribute
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def _date_value():
    """
    A function to get only the date of today. Used for setting the value of DateFields
    """
    return datetime.today().date()


class BooleanDescriptor:
    def __init__(self, field, value_function: Callable):
        self.field = field
        self.value_function = value_function
        self.datetime_name = field.attname
        self.bool_name = field.name

    def __get__(self, instance, cls=None):
        if not hasattr(instance.__dict__, self.bool_name):
            instance.__dict__[self.bool_name] = getattr(instance, self.datetime_name) is not None

        return instance.__dict__[self.bool_name]

    def __set__(self, instance, value):
        if value is False:
            instance.__dict__[self.datetime_name] = None

        if value and not instance.__dict__.get(self.bool_name):
            instance.__dict__[self.datetime_name] = self.value_function()

        instance.__dict__[self.bool_name] = value


class DatetimeDescriptor(DeferredAttribute):
    """
    Wrap the datetime property's descriptor to keep the boolean and datetime values in sync.
    """

    def __init__(self, field):
        super().__init__(field)
        self.datetime_name = field.attname
        self.bool_name = field.name

    def __set__(self, instance, value):
        if value is None:
            instance.__dict__[self.bool_name] = False
        else:
            instance.__dict__[self.bool_name] = True

        instance.__dict__[self.datetime_name] = value


class BooleanDateField(models.DateField):
    """
    A model field to track boolean values using a nullable date column.
    """

    descriptor_class = DatetimeDescriptor
    description = _("Boolean (Either True or False)")

    def __init__(self, *args, **kwargs):
        kwargs["null"] = True

        if kwargs.get("default"):
            kwargs["default"] = _date_value

        super().__init__(*args, **kwargs)

    def get_attname(self):
        return self.db_column or f"{self.name}_on"

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, BooleanDescriptor(self, _date_value))


class BooleanDateTimeField(models.DateTimeField):
    """
    A model field to track boolean values using a nullable datetime column.
    """

    descriptor_class = DatetimeDescriptor
    description = _("Boolean (Either True or False)")

    def __init__(self, *args, **kwargs):
        kwargs["null"] = True

        if kwargs.get("default"):
            kwargs["default"] = timezone.now

        super().__init__(*args, **kwargs)

    def get_attname(self):
        return self.db_column or f"{self.name}_at"

    def get_prep_value(self, value):
        return value

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, BooleanDescriptor(self, timezone.now))


class IsDatetimeTruthy(Lookup):
    """
    Look up a datetime field as "truthy"

    This is the reverse of the IsNull lookup.
    """

    lookup_name = "isset"
    prepare_rhs = False

    def as_sql(self, compiler, connection):
        if not isinstance(self.rhs, bool):
            raise ValueError("The QuerySet value for an isnull lookup must be True or False.")
        sql, params = self.process_lhs(compiler, connection)
        if self.rhs:
            return "%s IS NOT NULL" % sql, params
        else:
            return "%s IS NULL" % sql, params


BooleanDateField.register_lookup(IsDatetimeTruthy, "exact")
BooleanDateTimeField.register_lookup(IsDatetimeTruthy, "exact")
