import datetime as _date


class DBFunc:

    @property
    def now_utc_time(self):
        return lambda: _date.datetime.now(_date.timezone.utc)


db_funcs = DBFunc()
