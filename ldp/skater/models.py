from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

from userena.models import UserenaBaseProfile

from lib.human import seconds_to_human

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
        return self.user.trips.all().aggregate(models.Sum('duration'))['duration__sum']

    @cached_property
    def total_duration_human(self):
        return seconds_to_human(self.total_duration)

    @cached_property
    def total_distance(self):
        return self.user.trips.all().aggregate(models.Sum('distance'))['distance__sum']

    @cached_property
    def avg_distance(self):
        return self.user.trips.all().aggregate(models.Avg('distance'))['distance__avg']
    
    @cached_property
    def avg_speed(self):
        return "%0.2f" %(self.total_distance / self.total_duration * ( 60 *60 ))