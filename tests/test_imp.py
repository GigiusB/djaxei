import pytest

from djaxei import Importer


class TestEqual(object):

    @pytest.mark.django_db
    def test_equal_integer(self):
        Importer().xls_import(self.request.FILES['file'],
              models=[
                  'app1.demomodel1',
                  'app1.demomodel2',
                  'app1.demomodel3',
                  'app1.demomodel4'
                ]
        )
        from demoproject.app1.models import DemoModel1
        assert DemoModel1.objects.filter(pk=-1).count() == 0
