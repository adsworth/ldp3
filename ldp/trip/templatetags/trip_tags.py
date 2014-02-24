from datetime import datetime, date, time
from django import template

from trip.forms.forms import TripForm
register = template.Library()

@register.inclusion_tag('trip/create_form.html')
def trip_create_form(user):
    return {'trip_form': TripForm(initial= {'start': datetime.combine(date.today(), time()),
                                            'end': datetime.combine(date.today(), time())
                                            }),
            'user': user 
            }

