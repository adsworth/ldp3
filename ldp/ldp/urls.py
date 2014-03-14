from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from userena.views import ProfileListView

from trip.views import SkaterTripListView, TripListView, TripDetailView, TripCreateView, TripUpdateView
from ldp.views import skater_activities

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ldp.views.home', name='home'),
    url('^activity/', include('actstream.urls')),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^impressum/', TemplateView.as_view(template_name="impressum.html"), name='impressum'),
    url(r'^trips/?$', TripListView.as_view() , name='trip_list'),
    url(r'^trip/(?P<pk>\d+)/?$', TripDetailView.as_view() , name='trip_detail'),
    url(r'^trip/new/?$', TripCreateView.as_view() , name='trip_create'),
    url(r'^trip/edit/(?P<pk>\d+)/?$', TripUpdateView.as_view() , name='trip_edit'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<username>(?!signout|signup|signin)[\.\w-]+)/activities/$', skater_activities, name='skater_activities'),
    url(r'^(?P<username>(?!signout|signup|signin)[\.\w-]+)/trips/$', SkaterTripListView.as_view() , name='skater_trip_list'),
    url(r'^skater/', ProfileListView.as_view(), name='ldp3_profile_list'),
    url(r'^a/', include(admin.site.urls)),
    url(r'^', include('userena.urls')),
)
