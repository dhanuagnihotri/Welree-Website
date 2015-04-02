# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0027_auto_20150324_0306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('dateAndTime', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('photo', sorl.thumbnail.fields.ImageField(upload_to=b'editorial')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
    ]
