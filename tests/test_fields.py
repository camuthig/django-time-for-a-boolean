from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from tests import models


class TestField(TestCase):
    def test_field_values(self):
        e1 = models.Example.objects.create(datetime_field=True, date_field=True)

        self.assertTrue(e1.datetime_field)
        self.assertTrue(e1.date_field)

        e1.refresh_from_db()

        self.assertTrue(e1.datetime_field)
        self.assertTrue(e1.date_field)

        e1.datetime_field = False
        e1.date_field = False
        e1.save()

        self.assertFalse(e1.datetime_field)
        self.assertFalse(e1.date_field)

        e1.refresh_from_db()

        self.assertFalse(e1.datetime_field)
        self.assertFalse(e1.date_field)

    def test_lookup_using_boolean(self):
        e1 = models.Example.objects.create(datetime_field=True)
        e2 = models.Example.objects.create(date_field=True)

        self.assertEqual(e1, models.Example.objects.filter(datetime_field=True).get())
        self.assertEqual(e2, models.Example.objects.filter(date_field=True).get())
        self.assertEqual(2, models.Example.objects.filter(date_column_field=False).count())

    def test_lookup_using_datetime(self):
        e1 = models.Example.objects.create(datetime_field=True)
        e2 = models.Example.objects.create(date_field=True)

        self.assertEqual(e1, models.Example.objects.filter(datetime_field_at__isnull=False).get())
        self.assertEqual(e1, models.Example.objects.filter(datetime_field_at__lt=timezone.now() + timedelta(minutes=1)).get())
        self.assertEqual(e2, models.Example.objects.filter(date_field_on__isnull=False).get())

    def test_custom_column_is_used_for_date(self):
        e1 = models.Example.objects.create(datetime_column_field=True)

        self.assertEqual(e1, models.Example.objects.filter(datetime_column_field_by__isnull=False).get())

    def test_custom_column_is_used_for_datetime(self):
        e1 = models.Example.objects.create(date_column_field=True)

        self.assertEqual(e1, models.Example.objects.filter(date_column_field_after__isnull=False).get())

    def test_default_value_set_from_boolean(self):
        e1 = models.Example.objects.create()

        self.assertEqual(e1, models.Example.objects.filter(default_datetime_field=True).get())
        self.assertEqual(e1, models.Example.objects.filter(default_datetime_field_at__isnull=False).get())
        self.assertEqual(e1, models.Example.objects.filter(default_date_field=True).get())
        self.assertEqual(e1, models.Example.objects.filter(default_date_field_on__isnull=False).get())

    def test_lookup_fails_for_non_boolean(self):
        def _func():
            list(models.Example.objects.filter(default_date_field="true"))

        self.assertRaises(ValueError, _func)
