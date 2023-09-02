# Django Time for a Boolean

Inspired by the [Rails project of the same name](https://github.com/calebhearth/time_for_a_boolean/tree/master), this
package makes it possible to add a datetime or date field to your database but treat it as a boolean.

For example, let's say you want to soft-delete a model by adding a `deleted` field to it. Right now, you may not need to
know exactly when the record was deleted, but does it hurt to have that information, just in case? And so instead of
creating a boolean field in your database, you can create a datetime field and check it for `null`.

To use the field, just add it to your model.

```python
from django.db import models
from django.utils import timezone

from django_time_for_a_boolean import BooleanDateField
from django_time_for_a_boolean import BooleanDateTimeField

class MyModel(models.Model):
    deleted = BooleanDateTimeField()
    started = BooleanDateField()

# You can set the values as booleans
m = MyModel(deleted=True)
m.started = True

# You can filter models as booleans

MyModel.objects.filter(deleted=True)  # This will search for non-null values
MyModel.objects.filter(started=False)  # This will search for null values

# By default, datetime fields will use a `_at` suffix for the database column and
# date fields will use a `_on` suffix. You can filter using those fields as well.

MyModel.objects.filter(deleted_at__lte=timezone.now())
```
The database field can be overwritten using the `db_column` on the field.

```python
from django.db import models

from django_time_for_a_boolean import BooleanDateTimeField

class MyModel(models.Model):
    deleted = BooleanDateTimeField(db_column="deleted_on")
```
