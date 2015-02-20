# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0011_customuser_email_confirmed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jewelrycollection',
            unique_together=set([('owner', 'name')]),
        ),
    ]
