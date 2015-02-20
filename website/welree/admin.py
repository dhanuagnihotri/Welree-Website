from django.contrib import admin

from welree import models
from sorl.thumbnail.admin import AdminImageMixin

class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    actions = None

class JewelryItemAdmin(ImageAdmin):
    search_fields = ('description', 'description', 'url')
    list_display = ('description', 'owner', 'material', 'color', 'type')
    list_filter = ('material', 'type', 'color')

class JewelryCollectionAdmin(ImageAdmin):
    search_fields = ('name',)
    list_display = ('name', 'kind', 'owner')
    list_filter = ('kind',)

admin.site.register(models.JewelryItem, JewelryItemAdmin)
admin.site.register(models.JewelryCollection, JewelryCollectionAdmin)
admin.site.register(models.CustomUser)
