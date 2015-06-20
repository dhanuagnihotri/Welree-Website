# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0040_auto_20150620_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', sorl.thumbnail.fields.ImageField(upload_to=b'userphoto')),
                ('order', models.IntegerField(null=True, blank=True)),
                ('owner', models.ForeignKey(related_name='photos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
    ]
