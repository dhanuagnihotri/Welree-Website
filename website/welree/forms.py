from django import forms
from django.template import loader
from django.utils.http import int_to_base36
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.conf import settings

from django.utils.translation import ugettext, ugettext_lazy as _

from welree import models

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'is_designer']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

class CollectionForm(forms.ModelForm):
    kind = forms.ChoiceField(choices=models.JewelryCollection.KIND_CHOICES, widget=forms.HiddenInput())

    class Meta:
        model = models.JewelryCollection
        fields = ['name']

class JewelryItemForm(forms.ModelForm):
    class Meta:
        model = models.JewelryItem
        fields = ['collection', 'primary_photo', 'description', 'url', 'type', 'material', 'color', 'tags']

"""
class ConsumerJewelryItemForm(JewelryItemForm):
    class Meta:
        model = models.JewelryItem
        fields = ['collection', 'primary_photo', 'description', 'url', 'tags']
"""

class PasswordResetForm(forms.Form):
    error_messages = {
        'unknown': _("That e-mail address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': _("The user account associated with this e-mail "
                      "address cannot reset the password."),
    }
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = get_user_model().objects.filter(email__iexact=email,
                                               is_active=True)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any(user.has_unusable_password() for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            c = {
                'email': user.email,
                'domain': settings.WEBSITE_URL,
                'site_name': settings.WEBSITE_NAME,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': settings.WEBSITE_URL.split("://")[0],
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            user.email_user(subject, email)


