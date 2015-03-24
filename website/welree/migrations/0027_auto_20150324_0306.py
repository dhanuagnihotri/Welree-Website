# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0026_remove_jewelryitem_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jewelrycollection',
            name='items',
            field=models.ManyToManyField(related_name='collections', to='welree.JewelryItem'),
            preserve_default=True,
        ),
    ]
