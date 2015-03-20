# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0023_auto_20150317_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='jewelrycollection',
            name='items',
            field=models.ManyToManyField(to='welree.JewelryItem'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='collection',
            field=models.ForeignKey(related_name='jewelryitems', to='welree.JewelryCollection'),
            preserve_default=True,
        ),
    ]
