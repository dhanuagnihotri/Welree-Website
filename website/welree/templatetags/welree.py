from django.conf import settings
from django_jinja import library
from sorl.thumbnail.shortcuts import get_thumbnail
from functools import wraps

def debug_silence(error_output=''):
    def inner(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                if settings.DEBUG:
                    raise
                return error_output
        return wrapper
    return inner

@library.global_function
@debug_silence(error_output='')
def sorlthumbnail(file_, geometry_string, **options):
    try:
        im = get_thumbnail(file_, geometry_string, **options)
    except IOError:
        from raven.contrib.django.raven_compat.models import client
        client.captureException()
        im = None
    return im

@library.global_function
@debug_silence(error_output='')
def sorlimgtag(file_, geometry_string, **options):
    im = sorlthumbnail(file_, geometry_string, **options)
    return u"""<img src="{}" width="{}" height="{}" class="{}">""".format(im.url, im.width, im.height, options.get("classes", ""))

