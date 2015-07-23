# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0043_auto_20150630_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='featuredcollection',
            name='item1',
            field=models.ForeignKey(related_name='featured_first', default=10, to='welree.JewelryItem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='featuredcollection',
            name='item2',
            field=models.ForeignKey(related_name='featured_second', default=11, to='welree.JewelryItem'),
            preserve_default=False,
        ),
    ]
