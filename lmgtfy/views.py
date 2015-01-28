import csv

from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, resolve_url, HttpResponse
from django.views.generic import FormView, ListView

from lmgtfy.forms import MainForm
from lmgtfy.helpers import search_bing, check_valid_tld
from lmgtfy.models import Domain, DomainSearchResult


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
        domain = data['domain_base']
        domain_is_whitelisted = check_valid_tld(domain)
        if not domain_is_whitelisted:
            messages.info(
                self.request,
                "Sorry, we currently cannot search this domain (%s)." % domain
            )
            return HttpResponseRedirect(resolve_url('home'))

        search_done = search_bing(domain)

        if not search_done:
            messages.info(
                self.request,
                "We've already fetched these results today. Here they are!"
            )
        else:
            messages.info(
                self.request,
                "A background task has been created and you shall soon see the results!"
            )
        return HttpResponseRedirect(
            resolve_url('home')
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
        ).order_by('result')
        if fmt:
            qs = qs.filter(fmt=fmt)
        return qs

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['domain_name'] = self.kwargs['domain']
        qs = set(self.get_queryset().values_list('fmt', flat=True))
        context['file_formats'] = list(qs)
        return context


search_result_view = SearchResultView.as_view()


def get_csv(request, domain):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s.csv"' % domain
    writer = csv.writer(response)
    qs = DomainSearchResult.objects.filter(
        search_instance__domain__name=domain
    ).order_by('result').distinct()
    for result in qs:
        writer.writerow([result.title.encode("utf-8"), result.result.encode("utf-8")])
    return response
