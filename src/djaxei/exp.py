import os
from tempfile import NamedTemporaryFile

import xlsxwriter
from django.contrib.admin.utils import NestedObjects
from django.db import router
from django.utils.translation import ugettext_lazy as _


class Exporter:
    def __init__(self, tmpdir=None, **kwargs):
        self.tmpdir = tmpdir

    def xls_export(self, _models, root=None, root_qs=None):
        if (root and root_qs) or ((root or root_qs) is None):
            raise RuntimeError(_("Either a root object or a root queryset must be provided"))

        workbook = None
        try:
            workbookfile = NamedTemporaryFile(dir=self.tmpdir, delete=False)
            workbook = xlsxwriter.Workbook(workbookfile)

            sheets = {}

            lmodels = {}
            for k, v in _models.items():
                lname = k.lower()
                model_name = lname.rsplit('.')[1]
                lmodels[lname] = v
                sheets[model_name] = {'row_index': 1, 'sheet': workbook.add_worksheet(model_name)}
                sheets[model_name]['sheet'].write_row(0, 0, v)

            if root:
                root_qs = root._meta.model.objects.filter(pk=root.pk)

            using = router.db_for_write(root_qs.first()._meta.model)
            collector = NestedObjects(using=using)
            collector.collect(root_qs)

            def callback(obj):
                fields = lmodels.get(obj._meta.label_lower, None)
                if fields:
                    sheets[obj._meta.model_name]['sheet'].write_row(sheets[obj._meta.model_name]['row_index'], 0,
                                                                    [getattr(obj, x) for x in fields])
                    sheets[obj._meta.model_name]['row_index'] += 1

            collector.nested(callback)
            workbook.close()
            return workbookfile.name

        except Exception as e:
            if workbook:
                if not workbookfile.closed:
                    workbookfile.close()
                if os.path.exists(workbookfile.name):
                    os.remove(workbookfile.name)
            raise e
