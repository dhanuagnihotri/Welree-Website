# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0008_auto_20150211_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewelryitem',
            name='color',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jewelryitem',
            name='material',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jewelryitem',
            name='tags',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jewelryitem',
            name='type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
