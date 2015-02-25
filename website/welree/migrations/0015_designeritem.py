# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0014_jewelryitem_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignerItem',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('welree.jewelryitem',),
        ),
    ]
