# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0039_useractivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='_about_studio_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='about_studio',
            field=markupfield.fields.MarkupField(default=b'', help_text=b'<a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown syntax</a> allowed, but no raw HTML. Examples: **bold**, *italic*, and use asterisks followed by a space for bullets.', null=True, rendered_field=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='about_studio_markup_type',
            field=models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')]),
            preserve_default=True,
        ),
    ]
