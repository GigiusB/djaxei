# see https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
import pytest

from djaxei import Exporter


@pytest.mark.django_db
class TestEqual(object):

    def test_export(self, demomodel1):
        workbook_filename = Exporter().xls_export(
            {
                'app1.demomodel1': ['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic', 'date', 'nullable', 'choice'],
                # 'app1.DemoModel2': ['id', 'questionnaire_id', 'sortid', 'has_summary', ] + L(
                #     ['heading', 'text', 'long_text']),
                # 'app1.DemoModel3': ['id', 'questionpage_id', 'can_have_multiple_answers', 'number', 'type',
                #                            'checks'] + L(['short_desc', 'text', 'extra', 'footer']),
            },
            root=demomodel1
        )
        print(workbook_filename)
        from demoproject.app1.models import DemoModel1
        assert DemoModel1.objects.filter(pk=demomodel1.id).count() == 1

    # fk = models.ForeignKey(User,
    #                        on_delete=models.CASCADE,
    #                        blank=True, null=True)
    # char = models.CharField(max_length=255)
    # integer = models.IntegerField()
    # logic = models.BooleanField(default=False)
    # null_logic = models.NullBooleanField(default=None)
    # date = models.DateField()
    # nullable = models.CharField(max_length=255, null=True, default=None)
    # choice