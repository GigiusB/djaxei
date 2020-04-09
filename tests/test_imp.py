import pytest


class TestEqual(object):

    @pytest.mark.django_db
    def test_equal_integer(self):
        # Importer().xls_import(self.request.FILES['file'],
        #       models=[
        #           'questionnaire.questionnaire',
        #           'questionnaire.questionpage',
        #           'questionnaire.question',
        #           'questionnaire.choice'
        #         ]
        # )
        from demoproject.app1.models import DemoModel1
        assert DemoModel1.objects.filter(pk=-1).count() == 0
