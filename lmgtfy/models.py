from django.db import models


class Domain(models.Model):
    def __unicode__(self):
        return self.name

    name = models.URLField()


class DomainSearch(models.Model):
    uuid = models.CharField(max_length=36, default='')
    domain = models.ForeignKey(Domain)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)


class DomainSearchResult(models.Model):
    search_instance = models.ForeignKey(DomainSearch)
    title = models.TextField(verbose_name='Search result title')
    result = models.TextField(verbose_name='File URL')
    fmt = models.TextField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name='Format'
    )
    size = models.BigIntegerField(verbose_name='File size', default=0)
    content_type = models.CharField(max_length=128, default='')


class TLD(models.Model):
    '''
    This model is responsible for domain zones that
    are allowed to be searched through the system.
    '''
    name = models.CharField(max_length=36)

    def __unicode__(self):
        return '*.%s' % self.name
