from django.forms import ModelForm

import floppyforms
from timedelta.widgets import TimedeltaWidget

from trip.models import Trip
from trip.forms.widgets import SplitDateTimeWidget

class TripForm(floppyforms.ModelForm):
    class Meta:
        model = Trip
        exclude = ['skater', 'end', 'avg_speed']
        localized_fields = ('start', 'duration', 'distance')
        widgets = {
            'start': SplitDateTimeWidget(date_placeholder="DD.MM.YYYY", time_placeholder="HH:MM"),
            'duration': TimedeltaWidget(attrs={'placeholder':"1d 2h 3m 4s"}),
        }