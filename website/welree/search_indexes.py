from haystack import indexes

from welree import models

class JewelryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.JewelryItem

    def index_queryset(self, **kwargs):
        return self.get_model().objects.select_related()

class CollectionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.JewelryCollection

    def index_queryset(self, **kwargs):
        return self.get_model().objects.select_related()

class DesignerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.CustomUser

    def index_queryset(self, **kwargs):
        return self.get_model().objects.filter(is_designer=True).select_related()
