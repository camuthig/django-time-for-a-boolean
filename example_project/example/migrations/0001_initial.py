# Generated by Django 4.2.4 on 2023-09-02 04:57

from django.db import migrations
from django.db import models

import django_time_for_a_boolean.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Example",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deleted",
                    django_time_for_a_boolean.fields.BooleanDateTimeField(null=True),
                ),
                ("ended", django_time_for_a_boolean.fields.BooleanDateField(null=True)),
            ],
        ),
    ]