from haystack import indexes
from mypython.models import Module
from machine.models import Machine
from deep.models import Deep

class ModuleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    type = indexes.CharField(model_attr='type')

    def get_model(self):
        return Module

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class MachineIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Machine

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class DeepIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Deep

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
