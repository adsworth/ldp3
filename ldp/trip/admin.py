from django.contrib import admin
from trip.models import Trip

class TripAdmin(admin.ModelAdmin):
    pass

admin.site.register(Trip, TripAdmin)