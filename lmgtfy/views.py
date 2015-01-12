from urlparse import urlparse

from django.views.generic import FormView
from django.shortcuts import HttpResponseRedirect

from lmgtfy.forms import MainForm
from lmgtfy.helpers import get_yboss
from lmgtfy.models import Domain, DomainSearch, DomainSearchResult


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
            count = domain_search_latest.domainsearchresult_set.count()
            domains_and_latest_counts.append((domain.name, count))
        context['table_data'] = domains_and_latest_counts
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        url = data['search_field']
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        domain_db_record, domain_exists = Domain.objects.get_or_create(
            name=domain
        )

        domain_search_record = DomainSearch.objects.create(
            domain=domain_db_record
        )

        search_results = YBOSS.search('site:%s filetype:xls' % domain)
        result_model_objects = []

        for result in search_results:
            result_model_objects.append(DomainSearchResult(
                search_instance=domain_search_record,
                result=result['clickurl']
            ))

        if result_model_objects:
            DomainSearchResult.objects.bulk_create(
                result_model_objects
            )

        return HttpResponseRedirect(self.success_url)

main_view = MainView.as_view()
