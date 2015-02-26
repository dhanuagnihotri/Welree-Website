# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0015_designeritem'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='_bio_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=markupfield.fields.MarkupField(null=True, rendered_field=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio_markup_type',
            field=models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')]),
            preserve_default=True,
        ),
    ]
