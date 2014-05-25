"""Views for the outlets app."""
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect

from . import models


class OutletsListView(ListView):
    """Lists the outlets of one country."""
    model = models.Outlet

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug', '')
        if slug:
            self.country = get_object_or_404(models.OutletCountry, slug=slug)
        else:
            try:
                first_country = models.OutletCountry.objects.all()[0]
            except IndexError:
                raise Http404
            else:
                return redirect(reverse('outlets_list', kwargs={
                    'slug': first_country.slug}))
        return super(OutletsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(country=self.country)
