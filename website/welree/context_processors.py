import cjson
import collections
from django.conf import settings
from jinja2 import Markup

def pluralize(count, string, plural=None):
    if float(count) == 1:
        return u"%s %s" % (count, string)
    else:
        return u"%s %s" % (count, plural if plural else string+"s")

def processor(request):
    context = {
        'request': request,
        'pluralize': pluralize,
        'len': len,
        'str': str,
        'dir': dir,
        'zip': zip,
        'disqus_shortname': settings.DISQUS_SHORTNAME,
        'json': lambda s: Markup(cjson.encode(s)),
        'welree_facets': {
            'type': ['Rings', 'Necklaces & Pendants', 'Bracelets', 'Earrings', 'Brooches'],
            'color': ['Gold', 'Silver', 'Black', 'White', 'Red', 'Blue', 'Green', 'Grey', 'Brown', 'Orange', 'Pink', 'Purple', 'Turquoise', 'Yellow'],
            'material': ['Gold', 'Silver', 'Pearl', 'Gemstone', 'Beads', 'Aluminum', 'Copper', 'Stainless Steel', 'Titanium', 'Tungsten', 'Platinum'],
        },
        'user_collections': collections.defaultdict(list)
    }
    if request.user.is_authenticated():
        for coll in request.user.collections.all():
            context['user_collections'][coll.get_kind_display()].append(coll.name)
    return context

