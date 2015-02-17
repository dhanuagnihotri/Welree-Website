from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.template import defaultfilters

import uuid

from sorl.thumbnail import ImageField as SorlImageField

class CustomUser(AbstractUser):
    is_designer = models.BooleanField(default=False, verbose_name="I'm a jewelry designer", help_text="We'll use this to customize your experience on Welree.")
    
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

class DesignerJewelryManager(models.Manager):
    def get_queryset(self):
        return super(DesignerJewelryManager, self).get_queryset().filter(collection__kind=JewelryCollection.KIND_DESIGNER).exclude(primary_photo='')

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

    def __unicode__(self):
        return self.name

class JewelryItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="jewelryitems")
    collection = models.ForeignKey(JewelryCollection)
    primary_photo = SorlImageField(upload_to='jewelry')
    description = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True, verbose_name="Product link")

    material = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, help_text="Separate multiple hashtags with spaces")

    objects = models.Manager()
    curated = DesignerJewelryManager()

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return "{}/{}".format(reverse("item", kwargs={"pk": self.id}), defaultfilters.slugify(self.description))

