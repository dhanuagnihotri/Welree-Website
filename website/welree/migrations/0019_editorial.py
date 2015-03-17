# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0018_auto_20150226_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=63)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(null=True, blank=True)),
                ('photo', sorl.thumbnail.fields.ImageField(upload_to=b'editorial')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
