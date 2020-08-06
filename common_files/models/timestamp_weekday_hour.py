"""TimestampWeekdayHour class"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampWeekdayHour(models.Model):
    """Abstract base class TimestampWeekdayHour has weekday and times"""

    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    DAY_OF_WEEK = (
        (SUNDAY, _('Sunday')),
        (MONDAY, _('Monday')),
        (TUESDAY, _('Tuesday')),
        (WEDNESDAY, _('Wednesday')),
        (THURSDAY, _('Thursday')),
        (FRIDAY, _('Friday')),
        (SATURDAY, _('Saturday')),
    )

    NINE_AM = 900
    NINE_FIFTEEN_AM = 915
    NINE_THIRTY_AM = 930
    NINE_FORTYFIVE_AM = 945
    TEN_AM = 1000
    TEN_FIFTEEN_AM = 1015
    TEN_THIRTY_AM = 1030
    TEN_FORTYFIVE_AM = 1045
    ELEVEN_AM = 1100
    ELEVEN_FIFTEEN_AM = 1115
    ELEVEN_THIRTY_AM = 1130
    ELEVEN_FORTYFIVE_AM = 1145
    TWELVE_PM = 1200
    TWELVE_FIFTEEN_PM = 1215
    TWELVE_THIRTY_PM = 1230
    TWELVE_FORTYFIVE_PM = 1245
    ONE_PM = 1300
    ONE_FIFTEEN_PM = 1315
    ONE_THIRTY_PM = 1330
    ONE_FORTYFIVE_PM = 1345
    TWO_PM = 1400
    TWO_FIFTEEN_PM = 1415
    TWO_THIRTY_PM = 1430
    TWO_FORTYFIVE_PM = 1445
    THREE_PM = 1500
    THREE_FIFTEEN_PM = 1515
    THREE_THIRTY_PM = 1530
    THREE_FORTYFIVE_PM = 1545
    FOUR_PM = 1600
    FOUR_FIFTEEN_PM = 1615
    FOUR_THIRTY_PM = 1630
    FOUR_FORTYFIVE_PM = 1645
    FIVE_PM = 1700
    FIVE_FIFTEEN_PM = 1715
    FIVE_THIRTY_PM = 1730
    FIVE_FORTYFIVE_PM = 1745
    SIX_PM = 1800
    SIX_FIFTEEN_PM = 1815
    SIX_THIRTY_PM = 1830
    SIX_FORTYFIVE_PM = 1845
    SEVEN_PM = 1900
    SEVEN_FIFTEEN_PM = 1915
    SEVEN_THIRTY_PM = 1930
    SEVEN_FORTYFIVE_PM = 1945
    EIGHT_PM = 2000
    EIGHT_FIFTEEN_PM = 2015
    EIGHT_THIRTY_PM = 2030
    EIGHT_FORTYFIVE_PM = 2045
    NINE_PM = 2100
    NINE_FIFTEEN_PM = 2115
    NINE_THIRTY_PM = 2130
    NINE_FORTYFIVE_PM = 2145
    TEN_PM = 2200

    QUARTER_HOUR = (
        (NINE_AM, _('9:00 am')),
        (NINE_FIFTEEN_AM, _('9:15 am')),
        (NINE_THIRTY_AM, _('9:30 am')),
        (NINE_FORTYFIVE_AM, _('9:45 am')),
        (TEN_AM, _('10:00 am')),
        (TEN_FIFTEEN_AM, _('10:15 am')),
        (TEN_THIRTY_AM, _('10:30 am')),
        (TEN_FORTYFIVE_AM, _('10:45 am')),
        (ELEVEN_AM, _('11:00 am')),
        (ELEVEN_FIFTEEN_AM, _('11:15 am')),
        (ELEVEN_THIRTY_AM, _('11:30 am')),
        (ELEVEN_FORTYFIVE_AM, _('11:45 am')),
        (TWELVE_PM, _('12:00 pm')),
        (TWELVE_FIFTEEN_PM, _('12:15 pm')),
        (TWELVE_THIRTY_PM, _('12:30 pm')),
        (TWELVE_FORTYFIVE_PM, _('12:45 pm')),
        (ONE_PM, _('1:00 pm')),
        (ONE_FIFTEEN_PM, _('1:15 pm')),
        (ONE_THIRTY_PM, _('1:30 pm')),
        (ONE_FORTYFIVE_PM, _('1:45 pm')),
        (TWO_PM, _('2:00 pm')),
        (TWO_FIFTEEN_PM, _('2:15 pm')),
        (TWO_THIRTY_PM, _('2:30 pm')),
        (TWO_FORTYFIVE_PM, _('2:45 pm')),
        (THREE_PM, _('3:00 pm')),
        (THREE_FIFTEEN_PM, _('3:15 pm')),
        (THREE_THIRTY_PM, _('3:30 pm')),
        (THREE_FORTYFIVE_PM, _('3:45 pm')),
        (FOUR_PM, _('4:00 pm')),
        (FOUR_FIFTEEN_PM, _('4:15 pm')),
        (FOUR_THIRTY_PM, _('4:30 pm')),
        (FOUR_FORTYFIVE_PM, _('4:45 pm')),
        (FIVE_PM, _('5:00 pm')),
        (FIVE_FIFTEEN_PM, _('5:15 pm')),
        (FIVE_THIRTY_PM, _('5:30 pm')),
        (FIVE_FORTYFIVE_PM, _('5:45 pm')),
        (SIX_PM, _('6:00 pm')),
        (SIX_FIFTEEN_PM, _('6:15 pm')),
        (SIX_THIRTY_PM, _('6:30 pm')),
        (SIX_FORTYFIVE_PM, _('6:45 pm')),
        (SEVEN_PM, _('7:00 pm')),
        (SEVEN_FIFTEEN_PM, _('7:15 pm')),
        (SEVEN_THIRTY_PM, _('7:30 pm')),
        (SEVEN_FORTYFIVE_PM, _('7:45 pm')),
        (EIGHT_PM, _('8:00 pm')),
        (EIGHT_FIFTEEN_PM, _('8:15 pm')),
        (EIGHT_THIRTY_PM, _('8:30 pm')),
        (EIGHT_FORTYFIVE_PM, _('8:45 pm')),
        (NINE_PM, _('9:00 pm')),
        (NINE_FIFTEEN_PM, _('9:15 pm')),
        (NINE_THIRTY_PM, _('9:30 pm')),
        (NINE_FORTYFIVE_PM, _('9:45 pm')),
        (TEN_PM, _('10:00 pm')),
    )

    weekday = models.PositiveSmallIntegerField(choices=DAY_OF_WEEK)
    start_time = models.PositiveSmallIntegerField(choices=QUARTER_HOUR)
    end_time = models.PositiveSmallIntegerField(choices=QUARTER_HOUR)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='+')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='+')

    class Meta:
        abstract = True
