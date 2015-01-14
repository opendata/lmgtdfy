from datetime import datetime, timedelta

from django.conf import settings

from crispy_forms.layout import Submit
from yboss import YBoss

from lmgtfy.models import Domain, DomainSearch, DomainSearchResult
from lmgtfy.constants import FORMAT_CHOICES


class CleanSubmitButton(Submit):
    field_classes = 'btn btn-default'


def get_yboss():
    return YBoss(
        settings.CONSUMER_KEY,
        settings.CONSUMER_SECRET
    )


def search_yahoo(domain):
    domain_db_record, _created = Domain.objects.get_or_create(name=domain)

    YBOSS = get_yboss()
    format_string_part = ' OR '.join([
        'filetype:%s' % fmt for fmt in FORMAT_CHOICES
    ])
    search_string = 'site:%s (%s)' % (domain, format_string_part)
    search_results = YBOSS.search(search_string)
    result_model_objects = []

    # currently we are not allowing to search the same domain more than once per day
    recently_searched = DomainSearch.objects.filter(
        created_at__gte=datetime.now()-timedelta(days=1),
        domain=domain_db_record
    ).count()
    if recently_searched:
        return False

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
