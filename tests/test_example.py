import pytest


class TestEqual(object):

    @pytest.mark.django_db
    def test_equal_integer(self):
        from demoproject.app1.models import DemoModel1
        assert DemoModel1.objects.filter(pk=-1).count() == 0
