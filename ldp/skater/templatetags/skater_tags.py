from datetime import datetime, date, time

from django import template
from django.conf import settings
from django.contrib.auth.models import User

from skater.models import privacy_exclude_for_user


register = template.Library()

@register.inclusion_tag('skater/random_skater.html')
def random_skater(user):
    skater = User.objects.exclude(profile=None).exclude(profile__privacy__in=privacy_exclude_for_user(user)).order_by('?')[:1]
    if len(skater) <> 0:
        skater = skater[0]

    return {'skater':  skater }

