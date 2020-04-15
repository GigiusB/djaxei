import importlib
import random

import datetime

import factory
import logging

import pytest
from factory.fuzzy import FuzzyInteger, FuzzyDate, FuzzyChoice, FuzzyText

from demoproject.app1.models import DemoModel1, DemoModel2, DemoModel3, DemoModel4
from djaxei.providers import get_writer, get_implemetation_class


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
    char = FuzzyText(length=10, prefix='dm1_')
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
    for n in range(3):
        for master in records1:
            ret.append(DemoModel2Factory.create(fk=master))
    return ret


@pytest.fixture
def records3(records1):
    ret = []
    for n in range(3):
        for master in records1:
            ret.append(DemoModel3Factory.create(fk=master))
    return ret


@pytest.fixture
def records4(records2, records3):
    ret = []
    for n in range(15):
        master1 = random.choice(records2)
        master2 = random.choice(records3) if n % 3 != 0 else None
        ret.append(DemoModel4Factory.create(fk2=master1, fk3=master2))
    return ret


@pytest.fixture
def mocked_writer_factory():
    def _f(implementation=None):
        writer = get_writer(implementation)
        implementation = get_implemetation_class(writer)

        orig_write_data = writer.write_data
        results = {}

        def write_data(obj, data):
            writer._results.update(data)
            obj.orig_write_data(data)

        writer.write_data = write_data

        yield writer

    return _f

# @pytest.fixture
# def mocked_writer():
#     #def create_sheet(self, title=None, index=None)
#     #def append(self, row):
#
#     def get_mocked_append(original, results):
#         def _f(self, row):
#             results[self.title].append(row)
#             return original(self, row)
#         return _f
#
#     def get_mocked_create_sheet(original, results):
#         def _f(self, title=None, index=None):
#             results[title] = []
#             return original(self, title, index)
#         return _f
#
#
#     results = {}
#     from openpyxl import Workbook
#     original_create_sheet = Workbook.create_sheet
#     from openpyxl.worksheet.worksheet import Worksheet
#     original_append = Worksheet.append
#     Worksheet.append = get_mocked_append(original_append, results)
#     Workbook.create_sheet = get_mocked_create_sheet(original_create_sheet, results)
#     yield results
#     Workbook.create_sheet = original_create_sheet
#     Worksheet.append = original_append
