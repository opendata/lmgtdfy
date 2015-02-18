from django.conf.urls import patterns, url, include

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'lmgtfy.views.main_view', name='home'),
    url(r'^(?P<domain>[.a-zA-Z0-9-]+)/$', 'lmgtfy.views.search_result_view', name='domain_result'),
    url(r'^(?P<domain>[.a-zA-Z0-9-]+):(?P<fmt>\w+)/$', 'lmgtfy.views.search_result_view', name='domain_result_fmt'),
    url(r'^(?P<domain>[.a-zA-Z0-9-]+)/csv$', 'lmgtfy.views.get_csv', name='domain_result_download'),
)
