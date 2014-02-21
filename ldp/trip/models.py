from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _

from utils.choices import Choices
from utils.human import seconds_to_human

from django.conf import settings


class Trip(models.Model):
    TYPE_CHOICES = Choices((
                   ('push', 'PUSH', _('pushed')),
                   ('pump', 'PUMP', _('pumped')),
                   ('paddle', 'PADDLE', _('paddled')),
                 ))

    skater = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='trips')
    
    type = models.CharField(verbose_name=_('Type'), max_length=6, choices=TYPE_CHOICES, default=TYPE_CHOICES.PUMP)
    
    start = models.DateTimeField(verbose_name=_('Start time'))
    end = models.DateTimeField(verbose_name=_('End time'))
    
    distance = models.DecimalField(verbose_name=_('Distance'), max_digits=5, decimal_places=2)

    notes = models.TextField(verbose_name=_('Notes'), default='', blank=True)

    duration = models.IntegerField(verbose_name=_('Duration'), editable=False)
    avg_speed = models.DecimalField(_('Avg. Speed'), max_digits=5, decimal_places=2, editable=False)

    class Meta:
        ordering = ['-start']

    def clean(self):
        if self.start >= self.end:
            raise ValidationError("Start date ends to be before end date")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        delta = self.end - self.start
        self.duration = delta.seconds
        
        tick = self.distance / self.duration
        
        self.avg_speed = tick * 60 * 60

        super(Trip, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

    def __unicode__(self):
        return "%s trip from %s to %s distance %d" %(self.skater, str(self.start), str(self.end), self.distance)

    def get_absolute_url(self):
        return reverse('trip_detail', kwargs={'pk':self.id})
    
    def duration_human(self):
        return seconds_to_human(self.duration)
