import importlib
import os
from collections import OrderedDict
from contextlib import contextmanager
from datetime import date, datetime
from tempfile import NamedTemporaryFile

from django.contrib.admin.utils import NestedObjects
from django.db import router
from django.utils.translation import ugettext_lazy as _


# def value_conversion(value):
#     if value:
#         if isinstance(value, list):
#             value = [value_conversion(item) for item in value]
#         elif isinstance(value, date):
#             value = value.strftime('%b %d, %Y')
#         elif isinstance(value, datetime):
#             value = value.strftime('%b %d, %Y, %H:%M')
#         return value
#     return ''


    # def __init__(self, dest=None):
    #     self.workbookfile = dest or NamedTemporaryFile(dir=self.tmpdir, suffix=".xlsx", delete=False)
    #     raise Exception('unimplemented')






        # workbook = None
        # try:
        #     workbookfile = self.dest or NamedTemporaryFile(dir=self.tmpdir, suffix=".xlsx", delete=False)
        #     workbook = self.Workbook()
        #
        #     sheets = {}
        #
        #     lmodels = {}
        #     for k, v in _models.items():
        #         lname = k.lower()
        #         model_name = lname.rsplit('.')[1]
        #         lmodels[lname] = v
        #         sheets[model_name] = workbook.create_sheet(title=model_name)
        #         sheets[model_name].append(v)
        #
        #     if root:
        #         root_qs = root._meta.model.objects.filter(pk=root.pk)
        #
        #     using = router.db_for_write(root_qs.first()._meta.model)
        #     collector = NestedObjects(using=using)
        #     collector.collect(root_qs)
        #
        #     def callback(obj):
        #         fields = lmodels.get(obj._meta.label_lower, None)
        #         if fields:
        #             sheets[obj._meta.model_name].append([getattr(obj, x) for x in fields])
        #
        #     collector.nested(callback)
        #     del workbook['Sheet']
        #     workbook.save(workbookfile)
        #     return workbookfile.name
        #
        # except Exception as e:
        #     if workbook:
        #         if not workbookfile.closed:
        #             workbookfile.close()
        #         if os.path.exists(workbookfile.name):
        #             os.remove(workbookfile.name)
        #     raise e
from djaxei.providers import get_writer


class Exporter:
    def __init__(self, dest=None, tmpdir=None, implementation=None, **kwargs):
        self.tmpdir = tmpdir
        self.dest = dest
        self.implementation = implementation

    def xls_export(self, _models, root=None, root_qs=None):
        if (root and root_qs) or ((root or root_qs) is None):
            raise RuntimeError(_("Either a root object or a root queryset must be provided"))

        with get_writer(self.implementation) as writer:
            data = {}
            lmodels = {}
            for k, v in _models.items():
                lname = k.lower()
                model_name = lname.rsplit('.')[1]
                lmodels[lname] = v
                data[model_name] = [v, ]

            if root:
                root_qs = root._meta.model.objects.filter(pk=root.pk)

            using = router.db_for_write(root_qs.first()._meta.model)
            collector = NestedObjects(using=using)
            collector.collect(root_qs)

            def callback(obj):
                fields = lmodels.get(obj._meta.label_lower, None)
                if fields:
                    data[obj._meta.model_name].append([getattr(obj, x) for x in fields])

            collector.nested(callback)

            workbookfilename = writer.write_data(data)

        return workbookfilename


