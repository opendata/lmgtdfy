from __future__ import absolute_import

import datetime
import urllib

from celery import shared_task
from django.conf import settings
from django.core.exceptions import DoesNotExist

from bingpy import WebSearch

from lmgtfy.constants import FORMAT_CHOICES
from lmgtfy.models import Domain, DomainSearchResult, DomainSearch

def get_bing():
    return WebSearch(settings.BING_KEY)

@shared_task
def search_bing_task(domain_search_record):
    domain = domain_search_record.domain.name
    format_string_part = ' OR '.join([
        'filetype:%s' % fmt for fmt in FORMAT_CHOICES
    ])
    search_string = 'site:%s (%s)' % (domain, format_string_part)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0000")
    print('%s: Searching with query: "%s"', now, search_string)
    bing = get_bing()
    search_results = bing.search(search_string, settings.SEARCH_PER_QUERY)
    result_model_objects = []

    for result in search_results:
        result_url = result.url
        print("Gathering information about %s", result_url)
        file_format_part = result_url.split('.')[-1].lower()
        if file_format_part not in FORMAT_CHOICES:
            file_format = 'unknown'
        else:
            file_format = file_format_part

        # let's get the file size (or at least try to)
        try:
            file_connection = urllib.urlopen(result_url)
            file_info = file_connection.info()
            file_size = file_info.getheaders('Content-Length')[0]
            file_type = file_info.getheader('Content-Type')
        except:
            file_size = 0
            file_type = 'unknown'

        new_result = DomainSearchResult(
            search_instance=domain_search_record,
            result=result_url,
            fmt=file_format,
            title=result.title,
            size=int(file_size) / 1024,
            content_type=file_type
        )

        try:
            DomainSearchResult.objects.get(new_result)
            continue
        except DoesNotExist:
            result_model_objects.append(new_result)

        # if there are results, batch them up and save them as we iterate.
        if len(result_model_objects) >= 20:
            DomainSearchResult.objects.bulk_create( result_model_objects )
            result_model_objects = []
            
    # save any remaining results
    if result_model_objects:
        DomainSearchResult.objects.bulk_create( result_model_objects )
    
    domain_search_record.completed_at = datetime.datetime.now()
    domain_search_record.save()
    return True
