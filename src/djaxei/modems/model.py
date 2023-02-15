"""The base ModelModems."""
from django.db import models


class AbstractModelMoDem:
    def __init__(self, model, *args, **kwargs):
        """Model is either a Django Model or the model._meta.label_lower of a Django model."""
        if hasattr(model, '_meta'):
            self.model_label = model._meta.label_lower
        else:
            self.model_label = model.lower()
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
    def __init__(self, model, fields: list = None, loader=None, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.field_list = fields
        self.loader = loader

    def get_header(self):
        return [fname if isinstance(fname, str) else fname[0] for fname in self.field_list]

    def modulate(self, obj):
        """Serialise obj using the provided field_list in Modem init.

        Raise exception if no field_list provided.
        """
        if not self.field_list:
            raise RuntimeError('Field list is mandatory for modulate')
        row = []
        for field in self.field_list:
            if isinstance(field, str):
                row.append(getattr(obj, field))
            else:
                row.append(field[1](getattr(obj, field[0])))
        # sheets[obj._meta.label_lower].append(row)
        return row