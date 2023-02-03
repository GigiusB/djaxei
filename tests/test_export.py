# see https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
import json
import random
from tempfile import NamedTemporaryFile

import pytest
from dateutil.tz import UTC
from openpyxl.reader.excel import load_workbook

from demoproject.app1.models import DemoModel5, DemoModel4, DemoModel3, DemoModel2
from djaxei import Exporter


@pytest.mark.django_db
def test_exporter(recordset):
    from demoproject.app1.models import DemoModel1
    roots = random.choice(DemoModel1.objects.all())
    fx_dt = lambda dt: dt.replace(tzinfo=None)
    data = {
        'app1.demomodel1': ['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic',
                            'date', 'nullable', 'choice',
                            ('timestamp', fx_dt), ('j', json.dumps)],
        'app1.demomodel2': ['id', 'fk_id',  'integer'],
        'app1.DemoModel3': ['id', 'fk_id', 'char', 'integer'],
        'app1.DemoModel4': ['id',  'fk3_id', 'char', 'fk2_id', 'integer'],
    }

    exporter = Exporter(root=roots, rules=data)
    with NamedTemporaryFile(suffix='.xlsx') as fo:
        exporter.xls_export(fo)

        results = {}
        wb = load_workbook(filename=fo.name, read_only=True)
        for sheet in wb.worksheets:
            results[sheet.title] = []
            for row in sheet.rows:
                results[sheet.title].append([c.value for c in row])

    for k, v in data.items():
        data[k] = [[x if isinstance(x, str) else x[0] for x in v], ]
    obj = roots
    data['app1.demomodel1'].append([
        obj.id, obj.fk_id, obj.char, obj. integer, obj.logic, obj.null_logic,
        obj.date, obj.nullable, obj.choice,
        fx_dt(obj.timestamp),
        json.dumps(obj.j)]
    )
    for obj in DemoModel2.objects.filter(fk=roots):
        data['app1.demomodel2'].append([obj.id, obj.fk_id, obj.integer])
    for obj in DemoModel3.objects.filter(fk=roots):
        data['app1.DemoModel3'].append([obj.id, obj.fk_id, obj.char, obj.integer])
    for obj in DemoModel4.objects.all():
        data['app1.DemoModel4'].append(
            [obj.id, obj.fk3_id, obj.char, obj.fk2_id, obj.integer]
        )

    expected = {}
    for k, v in data.items():
        expected[k.lower()] = v[0] + sorted(v[1:], key=lambda x: x[0])

    for k, v in results.items():
        results[k] = v[0] + sorted(v[1:], key=lambda x: x[0])


    print(1)
    assert results == expected

    # from openpyxl import load_workbook
    # wb = load_workbook(workbook_filename)
    # assert set(wb.sheetnames) == set(['demomodel1', 'demomodel2', 'demomodel3', 'demomodel4',])
    # assert [[cell.value for cell in row] for row in wb['demomodel2'].rows] == \
    #        [data['app1.demomodel2'], ] + [list(x) for x in root.demomodel2_set.values_list(*data['app1.demomodel2'])]

