"""The base FieldModems."""
from django.db import models


class AbstractFieldMoDem:
    def modulate(self, obj: models.Model, context):
        pass

    def demodulate(self, obj, context):
        pass