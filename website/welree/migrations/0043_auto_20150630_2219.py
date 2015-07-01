# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('welree', '0042_auto_20150622_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cover_photo',
            field=sorl.thumbnail.fields.ImageField(help_text=b'A wide, high resolution image to display at the top of your profile.', null=True, upload_to=b'profiles', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(help_text=b'An optional business card sized logo for your profile.', null=True, upload_to=b'profiles', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(help_text=b"A photo of you that we'll display on your profile.", null=True, upload_to=b'profiles', blank=True),
            preserve_default=True,
        ),
    ]
