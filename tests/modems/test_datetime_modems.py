import datetime

import pytest
import pytz

from djaxei.modems.field import DatetimeNonAwareModem


class Dummy:
    pass

timezone = pytz.timezone("America/Los_Angeles")

@pytest.mark.parametrize(
    'input, expected',
    (
            pytest.param(
                datetime.datetime(year=2022, month=7, day=11, hour=14, minute=15, second=26,
                                  microsecond=324430, tzinfo=timezone), datetime.datetime(2022, 7, 11, 14, 15, 26),
                id='simple'
            ),
            pytest.param(
                datetime.datetime(year=2022, month=7, day=11, hour=14, minute=15, second=26,
                                  microsecond=324430), datetime.datetime(2022, 7, 11, 14, 15, 26),
                id='non-TZ-aware'
            ),
            pytest.param(
                datetime.datetime(year=2022, month=7, day=11, hour=14, minute=15, second=26, tzinfo=timezone), datetime.datetime(2022, 7, 11, 14, 15, 26),
                id='no-microseconds'
            )
    )
)
def test_valid_not_aware_datetime_modulate(input, expected):
    obj = Dummy()

    obj.example_field = input
    output = DatetimeNonAwareModem('example_field').modulate(obj)
    assert output == expected

    # NB: there is loss of information as DatetimeNonAwareModem does not support microseconds and TZ
    assert DatetimeNonAwareModem('example_field').demodulate(output) == input.replace(tzinfo=None, microsecond=0)
