from adminsortable.admin import SortableAdminMixin
from django.contrib import admin

from welree import models
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.admin import AdminImageMixin

def image_file(image, short_description='Primary thumbnail'):
    def image_thumb(self, obj):
        image = eval(image_thumb.image)
        if image:
            thumb = get_thumbnail(image.file, '356x200')
            return u'<img width="{}" height={} src="{}" />'.format(thumb.width, thumb.height, thumb.url)
        else:
            return "No Image"

    image_thumb.__dict__.update({'short_description': short_description,
                                 'allow_tags': True,
                                 'image': image})
    return image_thumb

class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    actions = None

class JewelryItemAdmin(ImageAdmin):
    search_fields = ('description', 'description', 'url')
    list_display = ('thumbnail', 'description', 'owner', 'material', 'color', 'type')
    list_filter = ('material', 'type', 'color')

    thumbnail = image_file('obj.primary_photo')

    class Media:
        css = {'all': ['/static/css/admin/admin.css']}

class DesignerItem(models.JewelryItem):
    class Meta:
        proxy = True

class DesignerItemAdmin(JewelryItemAdmin):
    def queryset(self, request):
        return self.model.objects.filter(collections__kind=models.JewelryCollection.KIND_DESIGNER)

    list_display = ('thumbnail', 'is_approved', 'description', 'owner', 'material', 'color', 'type')
    list_editable = ('is_approved',)

class JewelryCollectionAdmin(ImageAdmin):
    search_fields = ('name',)
    list_display = ('name', 'kind', 'owner')
    list_filter = ('kind',)

class EditorialAdmin(SortableAdminMixin, ImageAdmin):
    search_fields = ('category', 'title', 'url')
    list_filter = ('category',)
    list_display = ('thumbnail', 'category', 'title')

    thumbnail = image_file('obj.photo')

class EventAdmin(SortableAdminMixin, ImageAdmin):
    search_fields = ('category', 'title', 'url')
    list_filter = ('category',)
    list_display = ('thumbnail', 'category', 'title')

    thumbnail = image_file('obj.photo')

class FeaturedCollectionAdmin(SortableAdminMixin, ImageAdmin):
    thumbnail = image_file('obj.collection.photo')

    def queryset(self, request):
        qs = super(FeaturedCollectionAdmin, self).queryset(request)
        return qs.filter(collection__kind=models.JewelryCollection.KIND_DESIGNER)

admin.site.register(models.JewelryItem, JewelryItemAdmin)
admin.site.register(DesignerItem, DesignerItemAdmin)
admin.site.register(models.JewelryCollection, JewelryCollectionAdmin)
admin.site.register(models.CustomUser)
admin.site.register(models.Editorial, EditorialAdmin)
admin.site.register(models.FeaturedCollection, FeaturedCollectionAdmin)
admin.site.register(models.Event, EventAdmin)
