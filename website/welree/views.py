from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout as logout_user, login as login_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from haystack.query import SearchQuerySet
from haystack.utils import Highlighter

import cjson
import collections
import re
import urllib

from welree import models
from welree.forms import SignupForm, CollectionForm, JewelryItemForm, ProfileForm, DesignerProfileForm

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
    featuredobjects = models.FeaturedCollection.objects.select_related('collection')[:2]
    featuredcollections = [f.collection.annotated() for f in featuredobjects]
    for featured, collection in zip(featuredobjects, featuredcollections):
        collection.secondary = (featured.item1.primary_photo, featured.item2.primary_photo)
    return r2r("index.jinja", request, locals())

def events(request):
    events = models.Event.objects.all()
    return r2r("events.jinja", request, locals())

def editorial(request):
    editorials = models.Editorial.objects.all()
    return r2r("editorial.jinja", request, locals())

def designers(request):
    users = models.CustomUser.objects.filter(is_designer=True)
    user = request.user if request.user.is_authenticated() else False
    return r2r("designers.jinja", request, locals())

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
    related_collection = list(collection.items.exclude(id=item.id).exclude(primary_photo=None))[:6]
    related_similar = [similar.object for similar in SearchQuerySet().models(models.JewelryItem).more_like_this(item)][:6]
    return r2r('item.jinja', request, locals())

def collection(request, coll_pk):
    collection = get_object_or_404(models.JewelryCollection, pk=coll_pk)
    owner = collection.owner
    items = collection.items.all()
    return r2r('collection.jinja', request, locals())

def profile(request, pk):
    user = get_object_or_404(models.CustomUser, pk=pk)
    if user.is_designer:
        return profile_designer(request, user)
    collections = [c.annotated() for c in user.collections.all()[:10]]
    return r2r('consumer/profile.jinja', request, locals())

def profile_designer(request, user):
    collections = [c.annotated() for c in user.collections.all()[:10]]
    item_photos = user.jewelryitems.order_by('-id')[:5]
    photos = user.photos.all()
    return r2r('designer/profile.jinja', request, locals())

@login_required
def my(request):
    form_collection_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_DESIGNER if request.user.is_designer else models.JewelryCollection.KIND_IDEABOOK})
    collections = [c.annotated() for c in request.user.collections.order_by('-id')]
    try:
        cid = int(request.GET['collection'])
        collection = request.user.collections.get(id=cid)
        owner = collection.owner
        items = collection.items.all()
    except:
        collection = None

    followingcollections = models.JewelryCollection.objects.filter(owner__in=request.user.following.all()).order_by('-added')
    followingcollections = [c.annotated() for c in followingcollections]
    my_likes = models.JewelryLike.objects.filter(owner=request.user).order_by('-id')
    my_liked = models.JewelryLike.objects.filter(collection__owner=request.user).order_by('-id')
    followers = request.user.followers.all()
    my_activity = models.UserActivity.objects.filter(owner=request.user).order_by('-timestamp')

    relevant_follows = followers if request.user.is_designer else request.user.following.all()

    formClass = DesignerProfileForm if request.user.is_designer else ProfileForm
    from django.forms.models import inlineformset_factory
    photo_factory = inlineformset_factory(models.CustomUser, models.UserPhoto, exclude=["order"], extra=4, max_num=4, can_delete=False)
    inline_photos = photo_factory(instance=request.user, prefix="photos")

    profile_form = formClass(instance=request.user)
    if request.method == "POST":
        profile_form = formClass(request.POST, request.FILES, instance=request.user)
        inline_photos = photo_factory(request.POST, request.FILES, instance=request.user, prefix="photos")
        if profile_form.is_valid():
            profile_form.save()
            for form in inline_photos:
                instance = form.save(commit=False)
                if instance.photo:
                    instance.owner = request.user
                    instance.save()
            messages.success(request, 'You\'ve successfully updated your profile!')
            return redirect('my')

    return r2r('my.jinja', request, locals())

def search(request):
    query = request.GET.get('q', '').replace('.', '').replace("'", "").replace(",", "")
    selected_facets = request.GET.getlist('selected_facets')
    selected_facets_query = '&selected_facets='+u';&selected_facets='.join([urllib.quote(facet) for facet in selected_facets]) if selected_facets else ''
    facets_friendly = ' and '.join([f.replace("_exact:", " is ") for f in selected_facets])
    model_friendly = 'jewelry' if selected_facets else request.GET.get('model', '').lower()
    model = {'jewelry': 'JewelryItem', 'collection': 'JewelryCollection', 'designer': 'CustomUser'}.get(model_friendly)
    jewelry_only = model_friendly == 'jewelry'

    facets = collections.defaultdict(int)
    result_lists = collections.defaultdict(list)
    results = []
    #if query or selected_facets:
    sqs = SearchQuerySet().auto_query(query)
    if model:
        sqs = sqs.models(getattr(models, model))
    if jewelry_only:
        sqs = sqs.facet('material').facet('color').facet('type').facet('occasion').facet('style')
        for narrow in selected_facets:
            sqs = sqs.narrow(narrow)
        facet_counts = sqs.facet_counts()
        facet_lookup = {}
        for field, values in facet_counts['fields'].items():
            facet_lookup[field] = collections.defaultdict(int)
            for value, count in values:
                facet_lookup[field][value] = count
    results = [result.object for result in sqs if result.object]
    for obj in results:
        obj.data = obj.get_search_result()
        tag = obj.data["tag"].lower()
        if not model or model == tag:
            facets[tag] += 1

    # An empty search for designers should list them alphabetized.
    if model_friendly == 'designer' and not query:
        results = sorted(results, key=lambda r: r.last_name)

    return r2r("search_results.jinja", request, locals())

@login_required
def consumer_upload(request):
    collection = request.GET.get('collection')
    form_ideabook_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_IDEABOOK})
    form_jewelbox_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_JEWELBOX})
    form_jewelryitem_new = JewelryItemForm(owner=request.user, initial={'collection': collection})
    collections = request.user.collections.all()
    ideabooks = request.user.ideabooks.all()
    jewelboxes = request.user.jewelboxes.all()
    return r2r('consumer/upload.jinja', request, locals())

@login_required
def designer_upload(request):
    collection = request.GET.get('collection')
    form_collection_new = CollectionForm(initial={'kind': models.JewelryCollection.KIND_DESIGNER})
    form_jewelryitem_new = JewelryItemForm(owner=request.user, initial={'collection': collection})
    collections = request.user.collections.all()
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

@csrf_exempt
def github(request):
    from django.conf import settings
    import subprocess
    subprocess.check_call(["git", "pull"], cwd=settings.WEBSITE_DIR)
    subprocess.check_call(["pbdeploy"], cwd=settings.WEBSITE_DIR)
    return HttpResponse()
