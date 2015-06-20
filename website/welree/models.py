from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.template import defaultfilters
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

import uuid

from markupfield.fields import MarkupField
from sorl.thumbnail import ImageField as SorlImageField

MARKDOWN_ALLOWED = """<a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown syntax</a> allowed, but no raw HTML. Examples: **bold**, *italic*, and use asterisks followed by a space for bullets."""

class CustomUser(AbstractUser):
    is_designer = models.BooleanField(default=False, verbose_name="I'm a jewelry designer", help_text="We'll use this to customize your experience on Welree.")
    email_confirmed = models.BooleanField(default=False)
    bio = MarkupField(default="", markup_type="markdown", help_text=MARKDOWN_ALLOWED, blank=True, null=True)
    photo = SorlImageField(upload_to="profiles", blank=True, null=True)
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False)
    activity = generic.GenericRelation('UserActivity')
    about_studio = MarkupField(default="", markup_type="markdown", help_text=MARKDOWN_ALLOWED, blank=True, null=True)

    def email_user(self, subject, message, from_email=None, ignore_confirmed=False):
        if not (ignore_confirmed or self.email_confirmed):
            return False

        AbstractUser.email_user(self, subject, message, from_email)
        return True

    @property
    def ideabooks(self):
        return self.collections.filter(kind=JewelryCollection.KIND_IDEABOOK)

    @property
    def jewelboxes(self):
        return self.collections.filter(kind=JewelryCollection.KIND_JEWELBOX)

    @property
    def full_name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    @property
    def noun(self):
        return "User" if not self.is_designer else "Designer"

    def get_search_result(self):
        return {
            "tag": "designer",
            "title": self.full_name,
            "description": self.bio,
            "image": None
        }

    def get_absolute_url(self):
        return "{}{}/".format(reverse("profile", kwargs={"pk": self.id}), defaultfilters.slugify(self.full_name))
    
    @classmethod
    def signup(cls, signup_form):
        password = signup_form.cleaned_data['password']
        user = signup_form.save()
        user.username = user.email
        user.set_password(password)
        user.save()
        user = authenticate(username=user.username, password=signup_form.cleaned_data['password'])

        # Send email confirmation.
        email_confirm_url = reverse('email_confirm', args=[str(uuid.uuid4())])
        msg = "Thanks for signing up for Welree!\n\nPlease confirm your email address by clicking the following link: {0}{1}. You won't be able to receive further emails from us until confirming your address.\n\nIf you didn't sign up, take no action, and this is the last email you'll receive from us.\n\nThanks,\n{0}".format(settings.WEBSITE_URL, email_confirm_url)
        user.email_user("Welcome to Welree", msg, ignore_confirmed=True)
        return user

class UserActivity(models.Model):
    TYPE_FOLLOWED = 0
    TYPE_UNFOLLOWED = 1
    TYPE_CREATE_IDEABOOK = 2
    TYPE_MODIFY_IDEABOOK = 3
    TYPE_LIKE_PHOTO = 4
    TYPE_CHOICES = (
            (TYPE_FOLLOWED, "Followed"),
            (TYPE_UNFOLLOWED, "UnFollowed"),
            (TYPE_CREATE_IDEABOOK, "Create new Ideabook"),
            (TYPE_MODIFY_IDEABOOK, "Modify IdeaBook"),
            (TYPE_LIKE_PHOTO, "Liked photo"),
    )

    kind = models.IntegerField(choices=TYPE_CHOICES, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class Editorial(models.Model):
    category = models.CharField(max_length=63)
    title = models.CharField(max_length=255)
    url = models.URLField()
    photo = SorlImageField(upload_to='editorial')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return u"{} - {}".format(self.category, self.title)

    def get_search_result(self):
        return {
            "tag": "editorial",
            "title": self.title,
            "description": u'{}: {} @ {}'.format(self.category, self.title, self.url),
            "image": self.photo,
        }

    def get_absolute_url(self):
        return self.url

class Event(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    dateAndTime = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    photo = SorlImageField(upload_to='event')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return u"{} - {}".format(self.category, self.title)

class JewelryLike(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="likes", db_index=True)
    collection = models.ForeignKey('welree.JewelryCollection')
    item = models.ForeignKey('welree.JewelryItem')

    def get_primary_photo(self):
        return self.item.primary_photo

    def get_absolute_url(self):
        return self.item.get_absolute_collection_url(self.collection)

class FeaturedCollection(models.Model):
    collection = models.ForeignKey('welree.JewelryCollection')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ('order',)

    def __unicode__(self):
        return unicode(self.collection)

class DesignerJewelryManager(models.Manager):
    def get_queryset(self):
        return super(DesignerJewelryManager, self).get_queryset().filter(collections__kind=JewelryCollection.KIND_DESIGNER, is_approved=True).exclude(primary_photo='')

class JewelryCollection(models.Model):
    KIND_DESIGNER = 0
    KIND_JEWELBOX = 1
    KIND_IDEABOOK = 2
    KIND_CHOICES = (
            (KIND_DESIGNER, "Designer"),
            (KIND_JEWELBOX, "JewelBox"),
            (KIND_IDEABOOK, "IdeaBook"),
    )

    kind = models.IntegerField(choices=KIND_CHOICES, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="collections")
    name = models.CharField(max_length=63)
    description = models.TextField()
    items = models.ManyToManyField('welree.JewelryItem', related_name="collections")

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('owner', 'name'),)

    def annotated(self):
        self.annotated_photos = [item.primary_photo for item in self.items.all()[:3]]
        return self

    def get_absolute_url(self):
        return "{}{}/".format(reverse("collection", kwargs={"coll_pk": self.id}), defaultfilters.slugify(self.name))

    def get_search_result(self):
        first = self.items.first()
        return {
            "tag": "collection",
            "title": self.name,
            "description": u'{} "{}" by {}'.format(self.get_kind_display(), self.name, self.owner.full_name),
            "image": first and first.primary_photo
        }

    def __unicode__(self):
        return self.name

class JewelryItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="jewelryitems")
    primary_photo = SorlImageField(upload_to='jewelry')
    description = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True, verbose_name="Product link")

    type = models.CharField(max_length=255)
    style = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    occasion = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, help_text="Separate multiple hashtags with spaces", blank=True, null=True)

    is_approved = models.BooleanField(default=False)

    objects = models.Manager()
    curated = DesignerJewelryManager()

    def __unicode__(self):
        return self.description

    def get_search_result(self):
        return {
            "tag": "jewelry",
            "title": self.description,
            "description": self.description + u"<br/>Color: {} Material: {} Type: {}".format(self.color, self.material, self.type),
            "image": self.primary_photo
        }

    def get_absolute_url(self):
        return self.get_absolute_collection_url(self.collections.first())

    def get_absolute_collection_url(self, collection):
        return "{}{}/".format(reverse("item", kwargs={"item_pk": self.id, "coll_pk": collection.id}), defaultfilters.slugify(self.description))

