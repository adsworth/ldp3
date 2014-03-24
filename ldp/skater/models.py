from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

from userena.models import UserenaBaseProfile

from timedelta.helpers import nice_repr

def privacy_exclude_for_user(user):
    privacy = ['closed',]
    
    if user.is_authenticated() == False:
        privacy = privacy + ['registered', ]
    return privacy


class SkaterProfile(UserenaBaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                verbose_name=_('User'),
                                related_name='profile')
    age = models.SmallIntegerField(_('Age'), default=0, blank=True)

    website = models.CharField(_('Website'), max_length=255, blank=True)

    location = models.CharField(_('Location'), max_length=100, default='', blank=True)

    about_me = models.TextField(_('About me'), default='', blank=True)

    gear = models.TextField(_('Skate Gear'), default='', blank=True)

    def get_unit_of_measure_display(self):
        return 'km'

    @cached_property
    def number_of_trips(self):
        return self.user.trips.all().count()

    @cached_property
    def total_duration(self):
        _total = timedelta(0)
        for t in self.user.trips.all():
            _total = _total + t.duration
        return _total

    @cached_property
    def total_duration_human(self):
        return nice_repr(self.total_duration)

    @cached_property
    def total_distance(self):
        return self.user.trips.all().aggregate(models.Sum('distance'))['distance__sum']

    @cached_property
    def avg_distance(self):
        return self.user.trips.all().aggregate(models.Avg('distance'))['distance__avg']
    
    @cached_property
    def avg_speed(self):
        total_seconds = self.total_duration.days * 24 * 60 * 60 + self.total_duration.seconds
        if total_seconds > 0:
            return float(self.total_distance) / total_seconds * ( 60 * 60 )
        else:
            return None
