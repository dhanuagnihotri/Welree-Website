from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout as logout_user, login as login_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

import cjson
import re

from welree import models
from welree.forms import SignupForm, CollectionForm, JewelryItemForm

def r2r(template, request, data=None):
    data = data or {}
    data['error_msg'] = data.get('error_msg', '')
    return render_to_response(template, data, context_instance=RequestContext(request))

def superuser_required(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

def home(request):
    curated = models.JewelryItem.curated.order_by('-id')
    editorials = models.Editorial.objects.all()[:4]
    featuredcollections = [f.collection for f in models.FeaturedCollection.objects.select_related('collection')[:2]]
    for featured in featuredcollections:
        featured.annotated_photos = [item.primary_photo for item in featured.items.all()[:3]]
    return r2r("index.jinja", request, locals())

def login(request):
    def failure(msg):
        messages.error(request, msg)
        return r2r("login.jinja", request, locals())

    if request.method == "GET":
        return r2r("login.jinja", request, locals())
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login_user(request, user)
                # Redirect to a success page.
                return redirect("home")
            else:
                # Return a 'disabled account' error message
                return failure("This account has been disabled.")
        else:
            # Return an 'invalid login' error message.
            return failure("Invalid email address or password.")

def logout(request):
    logout_user(request)
    return redirect("home")

def signup(request):
    usermodel = get_user_model()
    signup_form = SignupForm()
    if request.method == "GET":
        return r2r("signup.jinja", request, locals())
    else:
        signup_form = SignupForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = models.CustomUser.signup(signup_form)
            if user is not None:
                login_user(request, user)
        else:
            return r2r("signup.jinja", request, locals())

        messages.success(request, "You've successfully signed up! Please confirm your email address in order to receive future communication from Welree.")

        return redirect("home")

def item(request, coll_pk, item_pk):
    item = get_object_or_404(models.JewelryItem, pk=item_pk)
    collection = get_object_or_404(models.JewelryCollection, pk=coll_pk)
    owner = item.owner
    related_collection = list(collection.items.exclude(id=item.id).exclude(primary_photo=None)[:3])
    related_similar = []
    return r2r('item.jinja', request, locals())

@login_required
def consumer_upload(request):
    form_ideabook_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_IDEABOOK})
    form_jewelbox_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_JEWELBOX})
    form_jewelryitem_new = JewelryItemForm(owner=request.user)
    collections = request.user.collections.all()
    ideabooks = request.user.ideabooks.all()
    jewelboxes = request.user.jewelboxes.all()
    return r2r('consumer/upload.jinja', request, locals())

@login_required
def designer_upload(request):
    form_collection_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_DESIGNER})
    form_jewelryitem_new = JewelryItemForm(owner=request.user)
    collections = request.user.collections.filter(kind=models.JewelryCollection.KIND_DESIGNER)
    return r2r('designer/upload.jinja', request, locals())

@login_required
def email_confirm(request, token):
    request.user.email_confirmed = True
    request.user.save()
    return r2r('email_confirmed.jinja', request, locals())

@login_required
def account(request):
    if request.method == "POST":
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']

        if pw1 or pw2:
            if pw1 == pw2:
                request.user.set_password(pw1)
                request.user.save()
            else:
                error = "Passwords do not match."
        message = "Settings successfully updated."

    return r2r("account.jinja", request, locals())

def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   post_reset_redirect=None,
                   from_email=None,
                   extra_context=None):

    from welree.forms import PasswordResetForm as password_reset_form
    from django.contrib.auth.tokens import default_token_generator as token_generator

    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            form.save(**opts)
            return redirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = { 'form': form }
    if extra_context is not None:
        context.update(extra_context)
    return r2r(template_name, request, context)

def password_reset_done(request):
    message = "We've e-mailed you your username and instructions for resetting your password to the e-mail address you submitted. You should be receiving it shortly."
    messages.success(request, message)
    return redirect('home')

