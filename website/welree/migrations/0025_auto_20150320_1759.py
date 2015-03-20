# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_m2m(apps, schema_editor):
    for item in apps.get_model('welree', 'JewelryItem').objects.all():
        collection = item.collection
        collection.items.add(item)

class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0024_auto_20150320_1758'),
    ]

    operations = [
            migrations.RunPython(populate_m2m),
    ]

