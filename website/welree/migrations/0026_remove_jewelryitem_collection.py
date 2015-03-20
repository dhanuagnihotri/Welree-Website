# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0025_auto_20150320_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jewelryitem',
            name='collection',
        ),
    ]
