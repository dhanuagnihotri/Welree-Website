# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0029_auto_20150402_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'event'),
            preserve_default=True,
        ),
    ]
