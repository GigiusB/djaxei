"""The base FieldModems."""
from datetime import datetime

import json

from django.db import models


class BaseFieldMoDem:
    def __init__(self, field_ref: str) -> None:
        self.field_ref = field_ref

    def get_field_header(self):
        return self.field_ref

    def modulate(self, obj: models.Model, mappings=None):
        """Modulate the value of the self.field_ref field of the provided Django model object."""
        return getattr(obj, self.field_ref)

    def demodulate(self, value, mappings=None):
        """Demodulate the self.field_ref value."""
        return value


class RemapperFieldModem(BaseFieldMoDem):

    def __init__(self, field_ref: str, mapping_key: str) -> None:
        super().__init__(field_ref)
        self.mapping_key = mapping_key

    def demodulate(self, value, mappings):
        ret = value
        if ret is not None:
            ret = mappings[self.mapping_key][value]
        return ret


class JsonToStringModem(BaseFieldMoDem):
    def modulate(self, obj: models.Model, mappings=None):
        return json.dumps(getattr(obj, self.field_ref))

    def demodulate(self, value, mappings=None):
        return json.loads(value)


class DatetimeNonAwareModem(BaseFieldMoDem):
    """A modem for nomalizin a TZ-aware datetime to a non-TZ-aware datetime.

    NB: there is loss of information as does not support microseconds and TZ
    """
    def modulate(self, obj: models.Model, mappings=None):
        dt: datetime = getattr(obj, self.field_ref)
        return dt.replace(tzinfo=None, microsecond=0)
