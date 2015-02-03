# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0002_customuser_is_designer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_designer',
            field=models.BooleanField(default=False, help_text=b"We'll use this to customize your experience on Welree.", verbose_name=b"I'm a jewelry designer"),
            preserve_default=True,
        ),
    ]
