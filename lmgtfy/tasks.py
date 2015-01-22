from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
from yboss import YBoss


from lmgtfy.constants import FORMAT_CHOICES
from lmgtfy.models import Domain, DomainSearchResult, DomainSearch


def get_yboss():
    return YBoss(
        settings.CONSUMER_KEY,
        settings.CONSUMER_SECRET
    )


@shared_task
def search_task(domain):
    domain_db_record, _created = Domain.objects.get_or_create(name=domain)
    format_string_part = ' OR '.join([
        'filetype:%s' % fmt for fmt in FORMAT_CHOICES
    ])
    search_string = 'site:%s (%s)' % (domain, format_string_part)
    YBOSS = get_yboss()
    search_results = YBOSS.search(search_string)
    result_model_objects = []
    domain_search_record = DomainSearch.objects.create(
        domain=domain_db_record
    )

    for result in search_results:
        result_url = result['clickurl']
        result_model_objects.append(DomainSearchResult(
            search_instance=domain_search_record,
            result=result_url,
            fmt=result_url.split('.')[-1]
        ))
    if result_model_objects:
        DomainSearchResult.objects.bulk_create(
            result_model_objects
        )
    return True
