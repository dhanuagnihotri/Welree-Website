# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0020_auto_20150317_0134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editorial',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='editorial',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
