# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0036_auto_20150512_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='JewelryLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.ForeignKey(to='welree.JewelryCollection')),
                ('item', models.ForeignKey(to='welree.JewelryItem')),
                ('owner', models.ForeignKey(related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
