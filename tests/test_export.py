# see https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
import json
import random
from collections.abc import Iterable
from tempfile import NamedTemporaryFile

import pytest
from demoproject.app1.models import (DemoModel1, DemoModel2,
                                     DemoModel3, DemoModel4,)
from django.db.models import Q, QuerySet
from openpyxl.reader.excel import load_workbook

from djaxei import Exporter
from djaxei.modems.model import FieldListModelMoDem


def root_generator(key):
    qs = DemoModel1.objects.all()
    return {
        1: random.choice(qs),
        2: qs.filter(id__in=random.sample(list(qs.values_list('id', flat=True)), 2)),
        3: random.sample(list(qs), 2)
    }[key]


class ExampleModelExporter(FieldListModelMoDem):

    def __init__(self, model, fields: list, *args, **kwargs):
        super().__init__(model, fields, *args, **kwargs)




@pytest.mark.parametrize(
    'root_fx_key, m1, m2, m3, m4',
    (
        pytest.param(
            1, 'app1.demomodel1', 'app1.demomodel2', 'app1.DemoModel3', 'app1.DemoModel4',
            id='strings'
        ),
        pytest.param(
            2, DemoModel1, DemoModel2, DemoModel3, DemoModel4,
            id='models'
        ),
        pytest.param(
            3, DemoModel1, 'app1.demomodel2', DemoModel3, DemoModel4,
            id='mixed'
        ),
    )
)
def test_exporter(root_fx_key, m1, m2, m3, m4, recordset):
    roots = root_generator(root_fx_key)

    fx_dt = lambda dt: dt.replace(tzinfo=None)
    modems = {
        ExampleModelExporter(
            model=m1,
            fields=['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic',
                            'date', 'nullable', 'choice',
                            ('timestamp', fx_dt), ('j', json.dumps)]
        ),
        ExampleModelExporter(
            m1,
            ['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic',
                            'date', 'nullable', 'choice',
                            ('timestamp', fx_dt), ('j', json.dumps)]
        ),
        ExampleModelExporter(
            m2,
            ['id', 'fk_id', 'integer']
        ),
        ExampleModelExporter(
            m3,
            ['id', 'fk_id', 'char', 'integer']
        ),
        ExampleModelExporter(
            m4,
            ['id', 'fk3_id', 'char', 'fk2_id', 'integer']
        ),
    }

    exporter = Exporter(root=roots, modems=modems)
    with NamedTemporaryFile(suffix='.xlsx') as fo:
        exporter.xls_export(fo)

        # Checks starts here

        results = {}
        wb = load_workbook(filename=fo.name, read_only=True)
        for sheet in wb.worksheets:
            results[sheet.title] = []
            for row in sheet.rows:
                results[sheet.title].append([c.value for c in row])

    if isinstance(roots, QuerySet):
        roots = list(roots.all())
    elif not isinstance(roots, Iterable):
        roots = [roots]
    root_class = roots[0].__class__
    root_model_name = root_class._meta.label_lower

    result_root_header = results[root_model_name][0]

    expected = list(root_class.objects.filter(id__in=[c.id for c in roots]).values())
    actual = [dict(zip(result_root_header, row)) for row in results[root_model_name][1:]]
    assert expected == actual

    dd = {}
    for k, v in data.items():
        if isinstance(k, str):
            k = k.lower()
        else:
            k = k._meta.label_lower
        dd[k] = [[x if isinstance(x, str) else x[0] for x in v], ]
    data = dd

    if not isinstance(roots, Iterable):
        roots = [roots]
    for obj in roots:
        data['app1.demomodel1'].append([
            obj.id, obj.fk_id, obj.char, obj. integer, obj.logic, obj.null_logic,
            obj.date, obj.nullable, obj.choice,
            fx_dt(obj.timestamp).replace(microsecond=0),
            json.dumps(obj.j)]
        )
    for obj in DemoModel2.objects.filter(fk__in=roots):
        data['app1.demomodel2'].append([obj.id, obj.fk_id, obj.integer])
    for obj in DemoModel3.objects.filter(fk__in=roots):
        data['app1.demomodel3'].append([obj.id, obj.fk_id, obj.char, obj.integer])
    for obj in DemoModel4.objects.filter(Q(fk2__fk__in=roots) | Q(fk3__fk__in=roots)):
        data['app1.demomodel4'].append(
            [obj.id, obj.fk3_id, obj.char, obj.fk2_id, obj.integer]
        )

    expected = {}
    for k, v in data.items():
        expected[k.lower()] = v[:1] + sorted(v[1:], key=lambda x: x[0])
    for k in expected['app1.demomodel1'][1:]:
        k[-2] = k[-2].replace(microsecond=0)

    for k, v in results.items():
        results[k] = v[:1] + sorted(v[1:], key=lambda x: x[0])
    for k in results['app1.demomodel1'][1:]:
        k[6] = k[6].date()
        k[-2] = k[-2].replace(microsecond=0)

    assert results == expected
