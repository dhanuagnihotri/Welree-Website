# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0006_jewelrycollection_jewelryitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jewelryitem',
            old_name='uploader',
            new_name='owner',
        ),
    ]
