from urlparse import urlparse

from django.views.generic import FormView, ListView
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.contrib import messages

from lmgtfy.forms import MainForm
from lmgtfy.helpers import get_yboss
from lmgtfy.models import Domain, DomainSearchResult
from lmgtfy.helpers import search_yahoo


YBOSS = get_yboss()


class MainView(FormView):
    template_name = 'main.html'
    form_class = MainForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        domains_and_latest_counts = []
        for domain in Domain.objects.all():
            domain_search_latest = domain.domainsearch_set.all().last()
            if not domain_search_latest:
                continue
            count = domain_search_latest.domainsearchresult_set.count()
            domains_and_latest_counts.append((domain.name, count))
        context['table_data'] = domains_and_latest_counts
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        url = data['domain']
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        search_done = search_yahoo(domain)
        if not search_done:
            messages.info(
                self.request,
                "We've already fetched these results today. Here they are!"
            )
        return HttpResponseRedirect(
            resolve_url('domain_result', domain)
        )

main_view = MainView.as_view()


class SearchResultView(ListView):
    template_name = 'result.html'
    model = DomainSearchResult
    success_url = '.'

    def get_queryset(self):
        qs = super(SearchResultView, self).get_queryset()
        try:
            domain = self.kwargs['domain']
            fmt = self.kwargs.get('fmt')
        except:
            raise Exception('Invalid url parameter has been passed.')
        qs = qs.filter(
            search_instance__domain__name=domain
        ).order_by('result').distinct()
        if fmt:
            qs = qs.filter(fmt=fmt)
        return qs

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['domain_name'] = self.kwargs['domain']
        return context


search_result_view = SearchResultView.as_view()
