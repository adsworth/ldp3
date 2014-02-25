from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime

from utils.choices import Choices
from utils.human import seconds_to_human

from django.conf import settings

from timedelta.fields import TimedeltaField
from timedelta.helpers import nice_repr

class Trip(models.Model):
    TYPE_CHOICES = Choices((
                   ('push', 'PUSH', _('pushed')),
                   ('pump', 'PUMP', _('pumped')),
                   ('paddle', 'PADDLE', _('paddled')),
                 ))

    skater = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trips')
    
    type = models.CharField(verbose_name=_('Type'), max_length=6, choices=TYPE_CHOICES, default=TYPE_CHOICES.PUMP)
    
    start_utc = models.DateTimeField(verbose_name=_('Start time'))
    end_utc = models.DateTimeField(verbose_name=_('End time'), editable=False)
    
    distance = models.DecimalField(verbose_name=_('Distance'), max_digits=5, decimal_places=2)

    notes = models.TextField(verbose_name=_('Notes'), default='', blank=True)

    duration = TimedeltaField(verbose_name=_('Duration'))
    avg_speed = models.DecimalField(_('Avg. Speed'), max_digits=5, decimal_places=2, editable=False)

    class Meta:
        ordering = ['-start_utc']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        
        self.end_utc = self.start_utc + self.duration
        
        tick = self.distance / self.duration.seconds
        
        self.avg_speed = tick * 60 * 60

        super(Trip, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

    def __unicode__(self):
        return "%s trip from %s to %s distance %d" %(self.skater, str(self.start), str(self.end), self.distance)

    @property
    def start(self):
        return localtime(self.start_utc)
    
    @property
    def end(self):
        return localtime(self.end_utc)
    
    def get_absolute_url(self):
        return reverse('trip_detail', kwargs={'pk':self.id})
    
    def duration_human(self):
        return nice_repr(self.duration)
