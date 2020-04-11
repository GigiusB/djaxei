import random

import datetime

import factory
import logging

import pytest
from factory.fuzzy import FuzzyInteger, FuzzyDate, FuzzyChoice, FuzzyText

from demoproject.app1.models import DemoModel1, DemoModel2, DemoModel3, DemoModel4


@pytest.fixture(scope='session')
def client(request):
    import django_webtest
    wtm = django_webtest.WebTestMixin()
    wtm.csrf_checks = False
    wtm._patch_settings()
    request.addfinalizer(wtm._unpatch_settings)
    app = django_webtest.DjangoTestApp()
    return app


def pytest_configure():
    logger = logging.getLogger("djaxei")
    handler = logging.NullHandler()
    logger.handlers = [handler]


CHOICES_IDS = [x[0] for x in DemoModel1.CHOICES]
class DemoModel1Factory(factory.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    date = FuzzyDate(datetime.date(2008, 1, 1))
    choice = FuzzyChoice(CHOICES_IDS)

    class Meta:
        model = DemoModel1


class DemoModel2Factory(factory.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm2_')

    class Meta:
        model = DemoModel2


class DemoModel3Factory(factory.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm3_')

    class Meta:
        model = DemoModel3


class DemoModel4Factory(factory.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm4_')

    class Meta:
        model = DemoModel4


@pytest.fixture
def demomodel1(db):
    ret = DemoModel1Factory.create()
    return ret


@pytest.fixture
def records1(db):
    ret = []
    for n in range(3):
        ret.append(DemoModel1Factory.create())
    return ret


@pytest.fixture
def records2(records1):
    ret = []
    for master in records1:
        ret.append(DemoModel2Factory.create(fk=master))
    return ret


@pytest.fixture
def records3(records1):
    ret = []
    for master in records1:
        ret.append(DemoModel3Factory.create(fk=master))
    return ret


@pytest.fixture
def records4(records2, records3):
    ret = []
    for n in range(8):
        master1 = random.choice(records2)
        master2 = random.choice(records3) if n % 3 !=0 else None
        ret.append(DemoModel4Factory.create(fk1=master1, fk2=master2))
    return ret


@pytest.fixture
def mocked_writer():
    def get_mocked_write_row(results):
        def mocked_write_row(self, row, col, data, cell_format=None):
            l = results.setdefault(self.name, [])
            l.append(dict(
                row=row,
                col=col,
                data=data,
                cell_format=cell_format
            ))
        return mocked_write_row

    results = {}
    from xlsxwriter.worksheet import Worksheet
    original = Worksheet.write_row
    Worksheet.write_row = get_mocked_write_row(results)
    yield results
    Worksheet.write_row = original
