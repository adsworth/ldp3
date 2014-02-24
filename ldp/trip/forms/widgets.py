from django import forms
from django.forms.util import to_current_timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

import floppyforms 

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

