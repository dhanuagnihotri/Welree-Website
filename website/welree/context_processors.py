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
        'list': list,
        'disqus_shortname': settings.DISQUS_SHORTNAME,
        'json': lambda o: Markup(cjson.encode(o)),
        'welree_facets': collections.OrderedDict((
            ('type', ['Rings', 'Necklaces & Pendants', 'Bracelets', 'Earrings', 'Brooches']),
            ('style', ['Modern', 'Contemporary', 'Traditional', 'Vintage']),
            ('color', ['Gold', 'Silver', 'Black', 'White', 'Red', 'Blue', 'Green', 'Grey', 'Brown', 'Orange', 'Pink', 'Purple', 'Turquoise', 'Yellow']),
            ('material', ['Gold', 'Silver', 'Pearl', 'Gemstone', 'Beads', 'Aluminum', 'Copper', 'Stainless Steel', 'Titanium', 'Tungsten', 'Platinum']),
            ('occasion', ['Wedding', 'Party', 'Casual', 'Formal']),
        )),
        'user_collections': collections.defaultdict(list)
    }
    if request.user.is_authenticated():
        for coll in request.user.collections.all():
            context['user_collections'][coll.get_kind_display()].append(coll.name)
        context['likes'] = list(request.user.likes.values_list('item_id', flat=True))
    else:
        context['likes'] = []
    return context

