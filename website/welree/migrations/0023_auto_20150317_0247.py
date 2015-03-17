# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0022_featuredcollection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jewelryitem',
            name='collection',
            field=models.ForeignKey(related_name='items', to='welree.JewelryCollection'),
            preserve_default=True,
        ),
    ]
