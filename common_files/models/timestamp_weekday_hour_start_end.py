"""TimestampWeekdayHourStartEnd class"""

from django.db import models

from common_files.models.timestamp_weekday_hour import TimestampWeekdayHour


class TimestampWeekdayHourStartEnd(TimestampWeekdayHour):
    """TimestampWeekdayHourStartEnd has weekday, start/end times and dates"""

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        abstract = True
