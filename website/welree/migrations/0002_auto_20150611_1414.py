# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0001_squashed_0045_auto_20150609_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jewelryitem',
            name='color',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='material',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='type',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='object_id',
            field=models.PositiveIntegerField(),
            preserve_default=True,
        ),
    ]
