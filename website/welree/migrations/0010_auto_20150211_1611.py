# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0009_auto_20150211_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jewelryitem',
            name='owner',
            field=models.ForeignKey(related_name='jewelryitems', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='tags',
            field=models.CharField(help_text=b'Separate multiple hashtags with spaces', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='url',
            field=models.URLField(null=True, verbose_name=b'Product link', blank=True),
            preserve_default=True,
        ),
    ]
