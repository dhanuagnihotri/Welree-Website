# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0032_jewelrycollection_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'profiles', blank=True),
            preserve_default=True,
        ),
    ]
