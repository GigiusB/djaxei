import datetime
import os
from collections import OrderedDict

import pytest

#from djaxei import Importer
from demoproject.app1.models import DemoModel1, DemoModel2, DemoModel3, DemoModel4


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


@pytest.mark.django_db
class TestImport(object):

    def test_importer(self, records4):
        dm1 = list(DemoModel1.objects.all())
        dm2 = list(DemoModel2.objects.all())
        dm3 = list(DemoModel3.objects.all())
        dm4 = list(DemoModel4.objects.all())
        fi = os.path.abspath(os.path.join(__file__, os.pardir, 'files', 'example_imp.xlsx'))
        storage = {}
        Importer().xls_import(fi,
          OrderedDict([
              ('demomodel1', row_loader_1(storage)),
              ('demomodel2', row_loader_2(storage)),
              ('demomodel3', row_loader_3(storage)),
              ('demomodel4', row_loader_4(storage)),
          ])
        )
        assert len(dm1) == DemoModel1.objects.count() - 1
        assert len(dm2) == DemoModel2.objects.count() - 3
        assert len(dm3) == DemoModel3.objects.count() - 3
        assert len(dm4) == DemoModel4.objects.count() - 7
