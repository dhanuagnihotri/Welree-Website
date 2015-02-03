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
