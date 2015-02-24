# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0013_auto_20150224_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewelryitem',
            name='is_approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
