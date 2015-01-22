from datetime import datetime, timedelta
from crispy_forms.layout import Submit

from lmgtfy.models import Domain, DomainSearch
from lmgtfy.tasks import search_task


class CleanSubmitButton(Submit):
    field_classes = 'btn btn-default'


def search_yahoo(domain):
    domain_db_record, _created = Domain.objects.get_or_create(name=domain)
    # currently we are do not allow to search the same domain more than once per day
    recently_searched = DomainSearch.objects.filter(
        created_at__gte=datetime.now()-timedelta(days=1),
        domain=domain_db_record
    ).count()
    if recently_searched:
        return False
    else:
        search_task.apply_async(kwargs={'domain': domain})
        return True
