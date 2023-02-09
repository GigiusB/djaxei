"""The base ModelModems."""
from django.db import models


class AbstractModelMoDem:
    def __init__(self, model, *args, **kwargs):
        """Model is either a Django Model or the model._meta.label_lower of a Django model."""
        if hasattr(model, '_meta'):
            self.model_label = model._meta.label_lower
        else:
            self.model_label = model
        self._extra_args = {
            'args': args,
            'kwargs': kwargs
        }

    def modulate(self, obj: models.Model, context):
        pass

    def demodulate(self, obj, context):
        pass


class FieldListModelMoDem(AbstractModelMoDem):
    """A ModelModem requiring a list of fields to serialize.

    The field in the list can be either be the str name of the field or a tuple consisting in:
    - the str name of the field
    - a function that will be passed the obj and the field name
    """
    def __init__(self, model, fields: list, *args, **kwargs):
        self.field_list = fields
        super().__init__(model, *args, **kwargs)