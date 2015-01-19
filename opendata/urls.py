from django.conf.urls import patterns, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lmgtfy.views.main_view', name='home'),
    url(r'^(?P<domain>[.a-z]+)/?$', 'lmgtfy.views.search_result_view', name='domain_result'),
    url(r'^(?P<domain>[.a-z]+):(?P<fmt>\w+)/?$', 'lmgtfy.views.search_result_view', name='domain_result_fmt'),

    # url(r'^admin/', include(admin.site.urls)),
)
