'''StartTimeListFilter class'''

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class StartTimeListFilter(admin.SimpleListFilter):
    '''StartTimeListFilter filters values larger than the requested value'''

    title = _('start time range')
    parameter_name = 'start_time'

    def lookups(self, request, model_admin):
        return (
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

    def queryset(self, request, queryset):
        '''Return queryset of an hour-long period from start time.'''
        if self.value() is None:
            return queryset.all()
        start = self.value()
        end = str(int(self.value()) + 100)
        return queryset.filter(start_time__gte=start, start_time__lte=end)
