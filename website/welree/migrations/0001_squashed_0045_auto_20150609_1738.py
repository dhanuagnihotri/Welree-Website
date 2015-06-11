# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import datetime
from django.utils.timezone import utc
import markupfield.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# welree.migrations.0025_auto_20150320_1759

class Migration(migrations.Migration):

    replaces = [(b'welree', '0001_initial'), (b'welree', '0002_customuser_is_designer'), (b'welree', '0003_auto_20150203_1526'), (b'welree', '0004_foobar'), (b'welree', '0005_delete_foobar'), (b'welree', '0006_jewelrycollection_jewelryitem'), (b'welree', '0007_auto_20150210_1614'), (b'welree', '0008_auto_20150211_0240'), (b'welree', '0009_auto_20150211_1532'), (b'welree', '0010_auto_20150211_1611'), (b'welree', '0011_customuser_email_confirmed'), (b'welree', '0012_auto_20150220_0219'), (b'welree', '0013_auto_20150224_1731'), (b'welree', '0014_jewelryitem_is_approved'), (b'welree', '0015_designeritem'), (b'welree', '0016_auto_20150226_1744'), (b'welree', '0017_auto_20150226_1746'), (b'welree', '0018_auto_20150226_1815'), (b'welree', '0019_editorial'), (b'welree', '0020_auto_20150317_0134'), (b'welree', '0021_auto_20150317_0204'), (b'welree', '0022_featuredcollection'), (b'welree', '0023_auto_20150317_0247'), (b'welree', '0024_auto_20150320_1758'), (b'welree', '0025_auto_20150320_1759'), (b'welree', '0026_remove_jewelryitem_collection'), (b'welree', '0027_auto_20150324_0306'), (b'welree', '0028_events'), (b'welree', '0029_auto_20150402_1340'), (b'welree', '0030_auto_20150402_1400'), (b'welree', '0028_auto_20150414_1427'), (b'welree', '0031_merge'), (b'welree', '0032_jewelrycollection_description'), (b'welree', '0033_auto_20150507_1333'), (b'welree', '0034_customuser_following'), (b'welree', '0033_customuser_photo'), (b'welree', '0035_merge'), (b'welree', '0036_auto_20150512_1626'), (b'welree', '0037_jewelrylike'), (b'welree', '0038_auto_20150528_1736'), (b'welree', '0039_useractivity'), (b'welree', '0040_auto_20150609_1345'), (b'welree', '0041_useractivity_object_id'), (b'welree', '0042_useractivity_content_type'), (b'welree', '0043_customuser_tag'), (b'welree', '0044_remove_customuser_tag'), (b'welree', '0045_auto_20150609_1738')]

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to=b'auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
                ('is_designer', models.BooleanField(default=False, help_text=b"We'll use this to customize your experience on Welree.", verbose_name=b"I'm a jewelry designer")),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
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
                ('url', models.URLField(null=True, verbose_name=b'Product link', blank=True)),
                ('collection', models.ForeignKey(to='welree.JewelryCollection')),
                ('owner', models.ForeignKey(related_name='jewelryitems', to=settings.AUTH_USER_MODEL)),
                ('color', models.CharField(default='', max_length=255)),
                ('material', models.CharField(default='', max_length=255)),
                ('tags', models.CharField(help_text=b'Separate multiple hashtags with spaces', max_length=255, null=True, blank=True)),
                ('type', models.CharField(default='', max_length=255)),
                ('is_approved', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='jewelrycollection',
            name='owner',
            field=models.ForeignKey(related_name='collections', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_confirmed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='jewelrycollection',
            unique_together=set([('owner', 'name')]),
        ),
        migrations.CreateModel(
            name='DesignerItem',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('welree.jewelryitem',),
        ),
        migrations.AddField(
            model_name='customuser',
            name='_bio_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=markupfield.fields.MarkupField(default=b'', help_text=b'<a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown syntax</a> allowed, but no raw HTML. Examples: **bold**, *italic*, and use asterisks followed by a space for bullets.', rendered_field=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='bio_markup_type',
            field=models.CharField(default=b'markdown', max_length=30, editable=False, choices=[(b'', b'--'), (b'markdown', b'markdown')]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=63)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('photo', sorl.thumbnail.fields.ImageField(upload_to=b'editorial')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='editorial',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='editorial',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='FeaturedCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('collection', models.ForeignKey(to='welree.JewelryCollection')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='collection',
            field=models.ForeignKey(related_name='items', to='welree.JewelryCollection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jewelrycollection',
            name='items',
            field=models.ManyToManyField(to=b'welree.JewelryItem'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jewelryitem',
            name='collection',
            field=models.ForeignKey(related_name='jewelryitems', to='welree.JewelryCollection'),
            preserve_default=True,
        ),  
        migrations.RemoveField(
            model_name='jewelryitem',
            name='collection',
        ),
        migrations.AlterField(
            model_name='jewelrycollection',
            name='items',
            field=models.ManyToManyField(related_name='collections', to=b'welree.JewelryItem'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=255)),
                ('dateAndTime', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('photo', sorl.thumbnail.fields.ImageField(upload_to=b'event')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='jewelryitem',
            name='occasion',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jewelryitem',
            name='style',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jewelrycollection',
            name='description',
            field=models.TextField(default='Lorem ipsum dolor sit amet, modus utamur adipisci id pri, nec verear maluisset theophrastus ea. Sonet eirmod et mei, ea deseruisse consequuntur eos, possim scripta ius ea. Adhuc aliquip disputando te cum, sed cu nonumy tincidunt accommodare, albucius maluisset scriptorem nec id. In vix ferri ullamcorper reprehendunt, errem propriae efficiendi ius ea, mazim vituperatoribus nam ex. Novum ponderum ea sea, cum ad veri euismod. Nonumy putent bonorum cum ei. Te deleniti sapientem molestiae per, cu eos sonet quaestio vulputate, ne assum feugiat ius. Et error omnesque instructior sit.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jewelrycollection',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 17, 33, 8, 69036, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jewelrycollection',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 7, 17, 33, 12, 956866, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='following_rel_+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'profiles', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=markupfield.fields.MarkupField(default=b'', help_text=b'<a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown syntax</a> allowed, but no raw HTML. Examples: **bold**, *italic*, and use asterisks followed by a space for bullets.', null=True, rendered_field=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='bio_markup_type',
            field=models.CharField(default=b'markdown', max_length=30, editable=False, blank=True, choices=[(b'', b'--'), (b'markdown', b'markdown')]),
            preserve_default=True,
        ),
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
        migrations.AlterField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(db_index=True, choices=[(0, b'Followed'), (1, b'UnFollowed'), (2, b'Create new Ideabook'), (3, b'Modify IdeaBook'), (4, b'Liked photo')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('object_id', models.PositiveIntegerField(default=0)),
                ('content_type', models.ForeignKey(default=0, to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
