# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0005_delete_foobar'),
    ]

    operations = [
        migrations.CreateModel(
            name='JewelryCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(db_index=True, choices=[(0, b'Designer'), (1, b'JewelBox'), (2, b'IdeaBook')])),
                ('name', models.CharField(max_length=63)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JewelryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary_photo', sorl.thumbnail.fields.ImageField(upload_to=b'jewelry')),
                ('description', models.CharField(max_length=255)),
                ('url', models.URLField(null=True, blank=True)),
                ('collection', models.ForeignKey(to='welree.JewelryCollection')),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
