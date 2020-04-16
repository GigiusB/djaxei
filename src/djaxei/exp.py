import os
from tempfile import NamedTemporaryFile

from django.contrib.admin.utils import NestedObjects
from django.db import router
from django.utils.translation import ugettext_lazy as _

from djaxei.providers.xlwt_provider import get_workbook_impl


class Exporter:
    def __init__(self, dest=None, tmpdir=None, **kwargs):
        self.tmpdir = tmpdir
        self.dest = dest

    def xls_export(self, _models, root=None, root_qs=None):
        if (root and root_qs) or ((root or root_qs) is None):
            raise RuntimeError(_("Either a root object or a root queryset must be provided"))

        workbook = None
        workbookfile = None
        try:
            workbookfile = self.dest or NamedTemporaryFile(dir=self.tmpdir, suffix=".xlsx", delete=False)

            sheets = {}

            lmodels = {}
            for k, v in _models.items():
                lname = k.lower()
                model_name = lname.rsplit('.')[1]
                lmodels[lname] = v
                sheets[model_name] = [v, ]

            if root:
                root_qs = root._meta.model.objects.filter(pk=root.pk)

            using = router.db_for_write(root_qs.first()._meta.model)
            collector = NestedObjects(using=using)
            collector.collect(root_qs)

            def callback(obj):
                fields = lmodels.get(obj._meta.label_lower, None)
                if fields:
                    sheets[obj._meta.model_name].append([getattr(obj, x) for x in fields])

            collector.nested(callback)

            Workbook = get_workbook_impl()()
            Workbook.write_data(workbookfile, sheets)

            return workbookfile.name

        except Exception as e:
            if workbook:
                if not workbookfile.closed:
                    workbookfile.close()
                if os.path.exists(workbookfile.name):
                    os.remove(workbookfile.name)
            raise e
