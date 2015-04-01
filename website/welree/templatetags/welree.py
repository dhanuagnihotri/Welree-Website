from django import template
from django.conf import settings
from django.http import QueryDict
from django_jinja import library
from functools import wraps
from jinja2 import Markup
from sorl.thumbnail.shortcuts import get_thumbnail

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
    return Markup(u"""<img src="{}" width="{}" height="{}" class="{}">""".format(im.url, im.width, im.height, options.get("classes", "")))


class GetRequestQueryStringNode(template.Node):
    def __init__(self, asvar=None):
        self.asvar = asvar

    def __repr__(self):
        return '<GetRequestQueryStringNode>'

    def render(self, context):
        request = context.get('request', None)
        if request is None:
            return ''
        qstring = request.GET.urlencode()
        if self.asvar:
            context[self.asvar] = qstring
            return ''
        return qstring


def qstring(parser, token):
    """
    Get the current request's query string.

    USAGE: {% qstring %} or {% qstring as current_qstring %}
    """
    bits = token.split_contents()
    if len(bits) not in (1, 3):
        raise template.TemplateSyntaxError("'%s' takes zero or 2 arguments "
                                           "(as var_name)." % bits[0])
    if len(bits) == 1:
        asvar = None
    else:
        asvar = bits[2]
    return GetRequestQueryStringNode(asvar)


def _qdict_del_keys(qdict, del_qstring):
    for key in del_qstring.split('&'):
        try:
            del qdict[key]
        except KeyError:
            pass
    return qdict


def _qdict_set_keys(qdict, set_qstring):
    set_qdict = QueryDict(set_qstring)
    for key, values in set_qdict.items():
        qdict[key] = set_qdict[key]
    return qdict


@library.global_function
def qdel(request, del_qstring):
    """
    Returns a query string w/o some keys, every value for each key gets deleted.

    More than one key can be specified using an & as separator:

    {{ my_qstring|qstring_del:"key1&key2" }}
    """
    qdict = QueryDict(request.META['QUERY_STRING'], mutable=True)
    return "{}?{}".format(request.path, _qdict_del_keys(qdict, del_qstring).urlencode())


@library.global_function
def qset(request, set_qstring):
    """
    Updates a query string, old values get deleted.

    {{ my_qstring|qstring_set:"key1=1&key1=2&key2=3" }}
    """
    qdict = QueryDict(request.META['QUERY_STRING'], mutable=True)
    return "{}?{}".format(request.path, _qdict_set_keys(qdict, set_qstring).urlencode())

