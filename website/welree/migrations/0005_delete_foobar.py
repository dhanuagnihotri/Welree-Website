# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0004_foobar'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Foobar',
        ),
    ]
