# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0032_jewelrycollection_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewelrycollection',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 17, 33, 8, 69036, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jewelrycollection',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 17, 33, 12, 956866, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
