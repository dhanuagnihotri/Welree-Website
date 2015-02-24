# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0012_auto_20150220_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jewelryitem',
            name='tags',
            field=models.CharField(help_text=b'Separate multiple hashtags with spaces', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
