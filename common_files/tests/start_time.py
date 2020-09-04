"""StartTimeListFilterTest class"""

from django.contrib.auth.models import User
from django.db import connection
from django.db.utils import ProgrammingError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from common_files.filters.start_time import StartTimeListFilter
from common_files.models.timestamp_weekday_hour import TimestampWeekdayHour


class StartTimeListFilterTest(TestCase):
    """Test StartTimeListFilter"""

    @classmethod
    def setUpClass(cls):
        class TimestampWeekdayHourChild(TimestampWeekdayHour):
            """TimestampWeekdayHourChild class test"""

            def __str__(self):
                return '{} {} - {}'.format(self.get_weekday_display(),
                                           self.get_start_time_display(),
                                           self.get_end_time_display())

            class Meta:
                app_label = 'common_files'

        cls.model = TimestampWeekdayHourChild

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.model)
            super().setUpClass()
        except ProgrammingError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.model)
            super().tearDownClass()
        except ProgrammingError:
            pass

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='fbar', email='fb@example.com')
        cls.model.objects.bulk_create([
            cls.model(weekday=0, start_time=900, end_time=1115,
                      created_by=user, modified_by=user),
            cls.model(weekday=2, start_time=1100, end_time=1415,
                      created_by=user, modified_by=user),
            cls.model(weekday=3, start_time=1300, end_time=1900,
                      created_by=user, modified_by=user),
            cls.model(weekday=5, start_time=1215, end_time=1545,
                      created_by=user, modified_by=user),
            cls.model(weekday=2, start_time=1200, end_time=1615,
                      created_by=user, modified_by=user)
            ])

    def test_lookups(self):
        """Test lookups"""
        lookup_values = (
            ('900', _('9:00 am - 10:00 am')),
            ('1000', _('10:00 am - 11:00 am')),
            ('1100', _('11:00 am - 12:00 pm')),
            ('1200', _('12:00 pm - 1:00 pm')),
            ('1300', _('1:00 pm - 2:00 pm')),
            ('1400', _('2:00 pm - 3:00 pm')),
            ('1500', _('3:00 pm - 4:00 pm')),
            ('1600', _('4:00 pm - 5:00 pm')),
            ('1700', _('5:00 pm - 6:00 pm')),
            ('1800', _('6:00 pm - 7:00 pm')),
            ('1900', _('7:00 pm - 8:00 pm')),
            ('2000', _('8:00 pm - 9:00 pm')),
        )
        stlf = StartTimeListFilter(None, {'start_time': None}, self.model,
                                   None)
        self.assertEqual(stlf.lookups(None, None), lookup_values)

    def test_queryset_with_none_value(self):
        """Test queryset with None value"""
        stlf = StartTimeListFilter(None, {'start_time': None}, self.model,
                                   None)
        self.assertIsNone(stlf.value())
        qs = stlf.queryset('', self.model.objects.all()).order_by('start_time')
        expected = ['<TimestampWeekdayHourChild: Sunday 9:00 am - 11:15 am>',
                    '<TimestampWeekdayHourChild: Tuesday 11:00 am - 2:15 pm>',
                    '<TimestampWeekdayHourChild: Tuesday 12:00 pm - 4:15 pm>',
                    '<TimestampWeekdayHourChild: Friday 12:15 pm - 3:45 pm>',
                    '<TimestampWeekdayHourChild: Wednesday 1:00 pm - 7:00 pm>']
        self.assertQuerysetEqual(qs, expected)

    def test_queryset_with_nonzero_value(self):
        """Test queryset with nonzero value"""
        stlf = StartTimeListFilter(None, {'start_time': 1100}, self.model,
                                   None)
        self.assertEqual(stlf.value(), 1100)
        qs = stlf.queryset('', self.model.objects.all()).order_by('start_time')
        expected = ['<TimestampWeekdayHourChild: Tuesday 11:00 am - 2:15 pm>',
                    '<TimestampWeekdayHourChild: Tuesday 12:00 pm - 4:15 pm>']
        self.assertQuerysetEqual(qs, expected)
