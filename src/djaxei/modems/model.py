"""The base ModelModems."""
from django.apps import apps
from django.db import models
from openpyxl.workbook import Workbook

from djaxei.modems.field import BaseFieldMoDem

TABNAME_LIMIT = 31


class AbstractModelMoDem:
    def __init__(self, model, *args, **kwargs):
        """Model is either a Django Model or the model._meta.label_lower of a Django model."""
        if hasattr(model, '_meta'):
            self.model_label = model._meta.label_lower
        else:  # Must be the label_lower
            self.model_label = model.lower()
        self._extra_args = {
            'args': args,
            'kwargs': kwargs
        }

    def modulate(self, obj: models.Model, context):
        pass

    def demodulate(self, obj, context):
        pass


class FieldListModelMoDemImporter:

    def __init__(self, remappings: dict, wb: Workbook, modem: AbstractModelMoDem) -> None:
        self.remappings = remappings
        self.worksheet = wb[modem.model_label[:TABNAME_LIMIT]]
        self.modem = modem
        self.manager = apps.get_model(modem.model_label).objects

    def run(self):
        pkpos, oldpk = None, None
        for i, row in enumerate(self.worksheet.rows):
            if i == 0:  # header
                headers = [c.value for c in row]
                if self.modem.pk in headers:
                    pkpos = headers.index(self.modem.pk)
                    headers.pop(pkpos)
                    self.modem.field_list.pop(pkpos)
            else:
                row = list(row)
                if pkpos is not None:
                    oldpk = row.pop(pkpos).value

                data = {}
                for z, h in enumerate(headers):
                    field = self.modem.field_list[z]
                    data[h] = row[z].value
                    if isinstance(field, BaseFieldMoDem):
                        data[h] = field.demodulate(data[h], self.remappings)

                new_obj = self.manager.create(**data)
                self.remappings[self.modem.model_label[:TABNAME_LIMIT]][oldpk] = new_obj.id


class FieldListModelMoDem(AbstractModelMoDem):
    """A ModelModem requiring a list of fields to serialize.

    The field in the list can be either be the str name of the field or a tuple consisting in:
    - the str name of the field
    - a function that will be passed the obj and the field name
    """
    def __init__(self, model, fields: list = None, pk='id', *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        self.field_list = fields
        self.pk = pk
        self._importer = None

    def get_importer(self, remappings: dict, wb: Workbook):
        if self._importer is None:
            self._importer = FieldListModelMoDemImporter(remappings, wb, self)
        return self._importer

    def get_header(self):
        ret = []
        for fname in self.field_list:
            if isinstance(fname, str):
                val = fname
            elif hasattr(fname, 'get_field_header'):
                val = fname.get_field_header()
            elif isinstance(fname, (tuple, list)):
                val = fname[0]
            ret.append(val)
        return ret

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
            elif hasattr(field, 'modulate'):
                row.append(field.modulate(obj))
            elif isinstance(field, (tuple, list)):
                row.append(field[1](getattr(obj, field[0])))
        return row

    def demodulate(self, obj, context):
        super().demodulate(obj, context)

