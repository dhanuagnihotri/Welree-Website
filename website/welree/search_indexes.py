from haystack import indexes

from welree import models

class JewelryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    material = indexes.CharField(model_attr="material", faceted=True, null=True)
    color = indexes.CharField(model_attr="color", faceted=True, null=True)
    type = indexes.CharField(model_attr="type", faceted=True, null=True)
    style = indexes.CharField(model_attr="style", faceted=True, null=True)
    occasion = indexes.CharField(model_attr="occasion", faceted=True, null=True)

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

class EditorialIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Editorial

    def index_queryset(self, **kwargs):
        return self.get_model().objects.select_related()
