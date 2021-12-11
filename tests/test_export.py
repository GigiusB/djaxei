# see https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
import random

import pytest
from django.db.models import Q

from demoproject.app1.models import DemoModel4
from djaxei import Exporter


@pytest.mark.django_db
class TestExport(object):

    def test_exporter(self, recordset):
        from demoproject.app1.models import DemoModel1
        root = random.choice(DemoModel1.objects.all())
        data = {
            'app1.demomodel1': ['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic', 'date', 'nullable', 'choice'],
            'app1.demomodel2': ['id', 'fk_id',  'integer'],
            'app1.DemoModel3': ['id', 'fk_id', 'char', 'integer'],
            'app1.DemoModel4': ['id',  'fk3_id', 'char', 'fk2_id', 'integer'],
        }

        workbook_filename = Exporter().xls_export(data, root=root)

        from openpyxl import load_workbook
        wb = load_workbook(workbook_filename)
        assert set(wb.sheetnames) == set(['demomodel1', 'demomodel2', 'demomodel3', 'demomodel4',])
        assert [[cell.value for cell in row] for row in wb['demomodel2'].rows] == \
               [data['app1.demomodel2'], ] + [list(x) for x in root.demomodel2_set.values_list(*data['app1.demomodel2'])]

