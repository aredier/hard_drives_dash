import datetime as dt
import os


def get_fake_today():
    if os.environ.get('CHARIOTS_LOCAL') == 'true':
        date_now = dt.datetime.utcnow()
        date_diff = dt.timedelta(
            days=date_now.day % 10,
            hours=date_now.hour,
            minutes=date_now.minute,
            seconds=date_now.second
        )
        return dt.datetime(year=2019, month=2, day=1) + date_diff
    return dt.datetime.utcnow() - dt.timedelta(days=200)