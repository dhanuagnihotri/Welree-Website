# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0003_auto_20150203_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foobar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('example', models.ImageField(upload_to=b'foobar')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
