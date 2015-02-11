# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0007_auto_20150210_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jewelrycollection',
            name='owner',
            field=models.ForeignKey(related_name='collections', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
