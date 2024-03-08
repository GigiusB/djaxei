import pytest
import random

from demoproject.app1.models import DemoModel1, VeryLongNameModelDemoModel4, DemoModel2, DemoModel3
from djaxei.exp import Exporter


def root_generator(key):
    qs = DemoModel1.objects.all()
    return {
        1: random.choice(qs),
        2: qs.filter(id__in=random.sample(list(qs.values_list('id', flat=True)), 2)),
        3: random.sample(list(qs), 2)
    }[key]



@pytest.mark.parametrize(
    'root_fx_key',
    (
        pytest.param(
            1,
            id='strings'
        ),
        pytest.param(
            2,
            id='models'
        ),
        pytest.param(
            3,
            id='mixed'
        ),
    )
)
def test_exporter_normalize_roots_to_list_of_objects(root_fx_key, recordset):
    roots = root_generator(root_fx_key)
    exporter = Exporter(root=roots, modems=[])

    if root_fx_key == 1:
        assert exporter.roots == [roots]
    elif root_fx_key == 2:
        assert exporter.roots == roots
    elif root_fx_key == 3:
        assert exporter.roots == roots
