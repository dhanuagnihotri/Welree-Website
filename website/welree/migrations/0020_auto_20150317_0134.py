# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0019_editorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editorial',
            name='url',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
