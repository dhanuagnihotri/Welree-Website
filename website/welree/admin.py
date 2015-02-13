from django.contrib import admin

from welree import models
from sorl.thumbnail.admin import AdminImageMixin

class ImageAdmin(AdminImageMixin, admin.ModelAdmin): pass
admin.site.register(models.JewelryItem, ImageAdmin)
admin.site.register(models.JewelryCollection, ImageAdmin)
admin.site.register(models.CustomUser)
