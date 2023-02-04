import importlib
import random

import datetime

import factory
import logging

import pytest
from dateutil.tz import UTC
from factory.fuzzy import FuzzyInteger, FuzzyDate, FuzzyChoice, FuzzyText, FuzzyDateTime

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
class DemoModel1Factory(factory.django.DjangoModelFactory):
    char = FuzzyText(length=10, prefix='dm1_')
    integer = FuzzyInteger(1000)
    date = FuzzyDate(datetime.date(2008, 1, 1))
    timestamp = FuzzyDateTime(start_dt=datetime.datetime(2008, 1, 1, 13, 44, 1, tzinfo=UTC))
    choice = FuzzyChoice(CHOICES_IDS)
    j = {
        'alfa': 1,
        'beta': {
            'gamma': 'delta'
        }
    }

    class Meta:
        model = DemoModel1


class DemoModel2Factory(factory.django.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm2_')

    class Meta:
        model = DemoModel2


class DemoModel3Factory(factory.django.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm3_')

    class Meta:
        model = DemoModel3


class DemoModel4Factory(factory.django.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm4_')

    class Meta:
        model = DemoModel4


class DemoModel5Factory(factory.django.DjangoModelFactory):
    integer = FuzzyInteger(1000)
    char = FuzzyText(length=10, prefix='dm5_')

    class Meta:
        model = DemoModel4


@pytest.fixture
def demomodel1(db):
    ret = DemoModel1Factory.create()
    return ret


@pytest.fixture
def records1(db):
    ret = []
    for n in range(5):
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
def records5(records2, records3):
    ret = []
    for n in range(15):
        master1 = random.choice(records2)
        master2 = random.choice(records3) if n % 3 != 0 else None
        ret.append(DemoModel5Factory.create(fk2=master1, fk3=master2))
    return ret


@pytest.fixture
def recordset(records4, records5):
    return records4 + records5
