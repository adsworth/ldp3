from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from trip.views import TripListView, TripDetailView, TripCreateView, TripUpdateView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ldp.views.home', name='home'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^impressum/', TemplateView.as_view(template_name="impressum.html"), name='impressum'),
    url(r'^trips/?$', TripListView.as_view() , name='trip_list'),
    url(r'^trip/(?P<pk>\d+)/?$', TripDetailView.as_view() , name='trip_detail'),
    url(r'^trip/new/?$', TripCreateView.as_view() , name='trip_create'),
    url(r'^trip/edit/(?P<pk>\d+)/?$', TripUpdateView.as_view() , name='trip_edit'),
    # url(r'^blog/', include('blog.urls')),
    (r'^skater/', include('userena.urls')),
    url(r'^a/', include(admin.site.urls)),
)
