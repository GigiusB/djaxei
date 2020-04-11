from random import random

import datetime

import factory
import logging

import pytest
from factory.fuzzy import FuzzyInteger, FuzzyDate, FuzzyChoice

from demoproject.app1.models import DemoModel1


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


@pytest.fixture
def demomodel1(db):
    ret = DemoModel1Factory.create()
    return ret