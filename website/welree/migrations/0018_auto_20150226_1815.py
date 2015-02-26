# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0017_auto_20150226_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=markupfield.fields.MarkupField(default=b'', help_text=b'<a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown syntax</a> allowed, but no raw HTML. Examples: **bold**, *italic*, and use asterisks followed by a space for bullets.', rendered_field=True),
            preserve_default=True,
        ),
    ]
