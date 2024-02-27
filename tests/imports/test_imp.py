import json
from django.apps import apps
from openpyxl.worksheet.worksheet import Worksheet

from pathlib import Path

import pytest

from djaxei import Importer
from demoproject.app1.models import DemoModel1, DemoModel2, DemoModel3, DemoModel4
from djaxei.modems.field import DatetimeNonAwareModem, JsonToStringModem, RemapperFieldModem
from djaxei.modems.model import FieldListModelMoDem


def row_loader_1(storage):
    def _f(data_dict):  # zip(header, fields)
        id = data_dict.pop('id')
        try:
            obj = DemoModel1.objects.create(**data_dict)
        except Exception as e:
            print(e)
        storage.setdefault(1, {})[id] = obj.id

    return _f


def row_loader_2(storage):
    def _f(data_dict):  # zip(header, fields)
        id = data_dict.pop('id')
        data_dict['fk_id'] = storage[1][data_dict['fk_id']]
        obj = DemoModel2.objects.create(**data_dict)
        storage.setdefault(2, {})[id] = obj.id

    return _f


def row_loader_3(storage):
    def _f(data_dict):  # zip(header, fields)
        id = data_dict.pop('id')
        data_dict['fk_id'] = storage[1][data_dict['fk_id']]
        obj = DemoModel3.objects.create(**data_dict)
        storage.setdefault(3, {})[id] = obj.id

    return _f


def row_loader_4(storage):
    def _f(data_dict):  # zip(header, fields)
        id = data_dict.pop('id')
        # fk2_id may have not been remapped
        data_dict['fk2_id'] = storage[2].get(data_dict['fk2_id'], data_dict['fk2_id'])
        # fk3_id may have not been remapped
        if data_dict['fk3_id'] is not None:
            data_dict['fk3_id'] = storage[3].get(data_dict['fk3_id'], data_dict['fk3_id'])
        obj = DemoModel4.objects.create(**data_dict)
        storage.setdefault(4, {})[id] = obj.id

    return _f


def loader_m1(mappings: dict, model_name: str, worksheet: Worksheet):
    klass = apps.get_model(*model_name.split('.'))

    for i, row in enumerate(worksheet.rows):
        if i == 0:  # header
            headers = [c.value for c in row][1:]
        else:
            oldid = row[0].value
            data = {h: row[z + 1].value for z, h in enumerate(headers)}

            data['j'] = json.loads(data['j'])

            new_obj = klass.objects.create(**data)
            mappings[model_name][oldid] = new_obj.id


def modifier_m1(row, *args):
    row['j'] = json.loads(row['j'])


def modifier_m2(row, mappings):
    row['fk_id'] = mappings['app1.demomodel2'][row['fk_id']]


def modifier_m3(row, mappings):
    row['fk_id'] = mappings['app1.demomodel3'][row['fk_id']]


def modifier_m4(row, mappings):
    row['fk_id'] = mappings['app1.demomodel4'][row['fk_id']]


def loader_m2(mappings: dict, model_name: str, worksheet: Worksheet):
    klass = apps.get_model(*model_name.split('.'))

    for i, row in enumerate(worksheet.rows):
        if i == 0:  # header
            headers = [c.value for c in row][1:]
        else:
            oldid = row[0].value
            data = {h: row[z + 1].value for z, h in enumerate(headers)}

            data['fk_id'] = mappings['app1.demomodel1'][data['fk_id']]

            new_obj = klass.objects.create(**data)
            mappings[model_name][oldid] = new_obj.id


@pytest.mark.django_db
class TestImport(object):

    def test_importer(self, recordset):
        existing_records = {
            'app1.demomodel1': list(DemoModel1.objects.all()),
            'app1.demomodel2': list(DemoModel2.objects.all()),
            'app1.demomodel3': list(DemoModel3.objects.all()),
            'app1.demomodel4': list(DemoModel4.objects.all()),
        }

        modems = [
            FieldListModelMoDem(
                model='app1.demomodel1',
                fields=['id', RemapperFieldModem('fk_id', 'app1.demomodel1'), 'char', 'integer', 'logic', 'null_logic',
                        'date', 'nullable', 'choice',
                        DatetimeNonAwareModem('timestamp'), JsonToStringModem('j')]
            ),
            FieldListModelMoDem(
                model='app1.demomodel2',
                fields=['id', RemapperFieldModem('fk_id', 'app1.demomodel1'), 'integer']
            ),
            FieldListModelMoDem(
                model='app1.demomodel3',
                fields=['id', RemapperFieldModem('fk_id', 'app1.demomodel1'), 'char', 'integer']
            ),
            FieldListModelMoDem(
                model='app1.demomodel4',
                fields=['id', RemapperFieldModem('fk3_id', 'app1.demomodel3'), 'char',
                        RemapperFieldModem('fk2_id', 'app1.demomodel2'), 'integer']
            ),
            # FieldListModelMoDem(
            #     'app1.demomodel2',
            #     ['id', 'fk_id', 'integer']
            # ),
            # FieldListModelMoDem(
            #     'app1.demomodel3',
            #     ['id', 'fk_id', 'char', 'integer']
            # ),
            # FieldListModelMoDem(
            #     'app1.demomodel4',
            #     ['id', 'fk3_id', 'char', 'fk2_id', 'integer']
            # ),
        ]
        importer = Importer(modems=modems)

        ret = importer.xls_import(Path(__file__).parent / 'exported.xlsx')
        assert DemoModel1.objects.count() == len(existing_records['app1.demomodel1']) + 1
        assert DemoModel2.objects.count() == len(existing_records['app1.demomodel2']) + 4
        assert DemoModel3.objects.count() == len(existing_records['app1.demomodel3']) + 4
        assert DemoModel4.objects.count() == len(existing_records['app1.demomodel4']) + 11

    # def test_importer(self, records4):
    #     dm1 = list(DemoModel1.objects.all())
    #     dm2 = list(DemoModel2.objects.all())
    #     dm3 = list(DemoModel3.objects.all())
    #     dm4 = list(DemoModel4.objects.all())
    #     fi = os.path.abspath(os.path.join(__file__, os.pardir, 'files', 'example_imp.xlsx'))
    #     storage = {}
    #     Importer().xls_import(fi,
    #       OrderedDict([
    #           ('demomodel1', row_loader_1(storage)),
    #           ('demomodel2', row_loader_2(storage)),
    #           ('demomodel3', row_loader_3(storage)),
    #           ('demomodel4', row_loader_4(storage)),
    #       ])
    #     )
    #     assert len(dm1) == DemoModel1.objects.count() - 1
    #     assert len(dm2) == DemoModel2.objects.count() - 3
    #     assert len(dm3) == DemoModel3.objects.count() - 3
    #     assert len(dm4) == DemoModel4.objects.count() - 7
