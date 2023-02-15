import json

import pytest

from demoproject.app1.models import DemoModel1, DemoModel2
from djaxei.modems.model import FieldListModelMoDem


@pytest.mark.parametrize(
    'm1, m2',
    (
        pytest.param(
            'app1.demomodel1', 'app1.DemoModel2',
            id='strings'
        ),
        pytest.param(
            DemoModel1, DemoModel2,
            id='models'
        ),
        pytest.param(
            DemoModel1, 'app1.demomodel2',
            id='mixed'
        ),
    )
)
def test_source_models_flavour(m1, m2):
    exp1 = FieldListModelMoDem(
            model=m1,
            fields=['id']
        )
    exp2 = FieldListModelMoDem(
            model=m2,
            fields=['id']
        )
    assert exp1.field_list == ['id']
    assert exp2.field_list == ['id']
    assert exp1.model_label == 'app1.demomodel1'
    assert exp2.model_label == 'app1.demomodel2'


def test_field_lists_get_header():
    exp1 = FieldListModelMoDem(
        model=DemoModel1,
        fields=['id', 'any....', ('alfa', str), ('bravo', json.dumps)]
    )
    assert exp1.field_list == ['id', 'any....', ('alfa', str), ('bravo', json.dumps)]
    assert exp1.get_header() == ['id', 'any....', 'alfa', 'bravo']


def test_field_lists_modulate(demomodel1):
    fx_dt = lambda dt: dt.replace(tzinfo=None)

    flist = ['id', 'fk_id', 'char', 'integer', 'logic', 'null_logic',
                'date', 'nullable', 'choice',
                ('timestamp', fx_dt), ('j', json.dumps)]

    exp1 = FieldListModelMoDem(
        model=DemoModel1,
        fields=flist
    )
    assert exp1.field_list == flist
    assert exp1.modulate(demomodel1) == [
        demomodel1.id,
        demomodel1.fk_id,
        demomodel1.char,
        demomodel1.integer,
        demomodel1.logic,
        demomodel1.null_logic,
        demomodel1.date,
        demomodel1.nullable,
        demomodel1.choice,
        fx_dt(demomodel1.timestamp),
        json.dumps(demomodel1.j)
    ]


def test_field_list_mandatory(demomodel1):
    exp1 = FieldListModelMoDem(
        model=DemoModel1,
        fields=[]
    )
    with pytest.raises(RuntimeError, match='Field list is mandatory for modulate'):
        exp1.modulate(demomodel1)
