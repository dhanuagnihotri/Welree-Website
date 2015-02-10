from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from sorl.thumbnail import ImageField as SorlImageField

class CustomUser(AbstractUser):
    is_designer = models.BooleanField(default=False, verbose_name="I'm a jewelry designer", help_text="We'll use this to customize your experience on Welree.")
    
    def email_user(self, subject, message, from_email=None, ignore_confirmed=False):
        if not (ignore_confirmed or self.email_confirmed):
            return False

        AbstractUser.email_user(self, subject, message, from_email)
        return True

class DesignerJewelryManager(models.Manager):
    def get_queryset(self):
        return super(DesignerJewelryManager, self).get_queryset().filter(collection__kind=JewelryCollection.KIND_DESIGNER)

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

class JewelryItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    collection = models.ForeignKey(JewelryCollection)
    primary_photo = SorlImageField(upload_to='jewelry')
    description = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)

    everything = models.Manager()
    objects = DesignerJewelryManager()
