# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0037_jewelrylike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
