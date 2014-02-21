from django.forms import ModelForm, SplitDateTimeWidget
from django.forms.util import to_current_timezone

import floppyforms 

from trip.models import Trip


class SplitDateTimeWidget(floppyforms.MultiWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None,
                 date_placeholder=None, time_placeholder=None):

        date_attrs = None
        time_attrs = None

        if date_placeholder:
            if not date_attrs:
                date_attrs = dict()
            else:
                date_attrs = attrs.copy()
            date_attrs['placeholder'] = date_placeholder

        if time_placeholder:
            if not time_attrs:
                time_attrs = dict()
            else:
                date_attrs = attrs.copy()
            time_attrs['placeholder'] = time_placeholder

        widgets = (floppyforms.widgets.DateInput(attrs=date_attrs, format=date_format),
                   floppyforms.widgets.TimeInput(attrs=time_attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

class TripForm(floppyforms.ModelForm):
    class Meta:
        model = Trip
        exclude = ['skater', 'duration', 'avg_speed']
        localized_fields = ('start', 'end', 'distance')
        widgets = {
            'start': SplitDateTimeWidget(date_placeholder="DD.MM.YYYY", time_placeholder="HH:MM"),
            'end': SplitDateTimeWidget(date_placeholder="DD.MM.YYYY", time_placeholder="HH:MM"),
        }
