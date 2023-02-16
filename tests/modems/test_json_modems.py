import pytest

from djaxei.modems.field import JsonToStringModem

class Dummy:
    pass


@pytest.mark.parametrize(
    'input, expected',
    (
            pytest.param(
                {'A': 1}, '{"A": 1}',
                id='simple'
            ),
            pytest.param(
                {}, '{}',
                id='empty'
            ),
            pytest.param(
                'abc123', '"abc123"',
                id='string'
            ),
    )
)
def test_valid_json_modulate(input, expected):
    obj = Dummy()

    obj.example_field = input
    output = JsonToStringModem('example_field').modulate(obj)
    assert output == expected

    assert JsonToStringModem('example_field').demodulate(output) == input
