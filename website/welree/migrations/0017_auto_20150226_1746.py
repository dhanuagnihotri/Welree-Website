# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0016_auto_20150226_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=markupfield.fields.MarkupField(default=b'', rendered_field=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bio_markup_type',
            field=models.CharField(default=b'markdown', max_length=30, editable=False, choices=[(b'', b'--'), (b'markdown', b'markdown')]),
            preserve_default=True,
        ),
    ]
