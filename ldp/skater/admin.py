from django.contrib import admin

from guardian.admin import GuardedModelAdmin
from userena.utils import get_profile_model

try:
    admin.site.unregister(get_profile_model())
except admin.sites.NotRegistered:
    pass

admin.site.register(get_profile_model(), GuardedModelAdmin)
