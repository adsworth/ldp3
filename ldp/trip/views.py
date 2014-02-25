from datetime import datetime, date, time

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView


from trip.forms.forms import TripForm
from trip.models import Trip

class SortMixin(object):
    """
    View mixin which provides sorting for ListView.
    """
    default_sort_param = None
    param_name_sort = 'sort_by'

    def sort_queryset(self, qs, sort_by, descending):
        return qs

    def get_default_sort_param(self):
        if self.default_sort_param is None:
            raise ImproperlyConfigured(
                "'SortMixin' requires the 'default_sort_param' attribute "
                "to be set.")
        return self.default_sort_param

    def get_sort_param(self):
        return self.request.GET.get(self.param_name_sort, self.get_default_sort_param())

    def get_sort_options(self):
        sort_by = self.get_sort_param()

        descending = False
        if sort_by[0] == '-':
            sort_by = sort_by[1:]
            descending = True
        
        return (sort_by, descending)

    def get_queryset(self):
        return self.sort_queryset(
            super(SortMixin, self).get_queryset(),
            *self.get_sort_options())

    def get_context_data(self, *args, **kwargs):
        context = super(SortMixin, self).get_context_data(*args, **kwargs)
        context.update({
            'sort_by': self.get_sort_param(),
        })
        return context

class FilterMixin(object):
    """
    View mixin which provides filtering for ListView.
    """
    filter_url_kwarg = 'filter'
    default_filter_param = None

    def get_default_filter_param(self):
        if self.default_filter_param is None:
            raise ImproperlyConfigured(
                "'FilterMixin' requires the 'default_filter_param' attribute "
                "to be set.")
        return self.default_filter_param

    def filter_queryset(self, qs, filter_param):
        """
        Filter the queryset `qs`, given the selected `filter_param`. Default
        implementation does no filtering at all.
        """
        return qs

    def get_filter_param(self):
        return self.kwargs.get(self.filter_url_kwarg,
                               self.get_default_filter_param())

    def get_queryset(self):
        return self.filter_queryset(
            super(FilterMixin, self).get_queryset(),
            self.get_filter_param())

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        context.update({
            'filter': self.get_filter_param(),
        })
        return context

class TripListView(SortMixin, ListView):
    default_sort_param = ('-start')
    param_name_sort = 's'

    model = Trip
    paginate_by = 20

    def sort_queryset(self, qs, sort_by, descending):
        if sort_by == 'dist':
            qs = qs.order_by('distance')
        elif sort_by == 'skater':
            qs = qs.order_by('skater')
        elif sort_by == 'start':
            qs = qs.order_by('start_utc')

        if descending == True:
            qs = qs.reverse()
        return qs

    def get_queryset(self):
        privacy = ['closed',]

        if self.request.user.is_authenticated() == False:
            privacy = privacy + ['registered', ]
            
        return super(TripListView, self).get_queryset().exclude(skater__profile__privacy__in=privacy)

class TripCreateView(CreateView):
    model = Trip
    context_object_name = 'trip'
    form_class = TripForm
#    fields = ['name']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TripCreateView, self).dispatch(*args, **kwargs)
    
#    def form_valid(self, form):
#        object = form.save(commit=False)
#        object.skater = self.request.user
#        object.save()
#        return super(TripCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        _kwargs = super(TripCreateView, self).get_form_kwargs()
        
        if not _kwargs['instance']:
            _kwargs['instance'] = Trip(skater=self.request.user)
        
        return _kwargs
    
    def get_success_url(self):
        return super(TripCreateView, self).get_success_url()

    def get_initial(self):
        return {'start': datetime.combine(date.today(), time()),
                'end': datetime.combine(date.today(), time())
                }


class TripUpdateView(UpdateView):
    model = Trip
    context_object_name = 'trip'
    form_class = TripForm

    def get_success_url(self):
        return super(TripUpdateView, self).get_success_url()


class TripDetailView(DetailView):
    model = Trip
    context_object_name = 'trip'

    def get_object(self, *args, **kwargs):
        _object = super(TripDetailView, self).get_object(*args, **kwargs)
        
        if _object.skater.profile.privacy == 'registered' and \
           self.request.user.is_authenticated() == False:
            raise PermissionDenied
        elif _object.skater.profile.privacy == 'closed' and \
             _object.skater <> self.request.user:
            raise PermissionDenied

        return _object
