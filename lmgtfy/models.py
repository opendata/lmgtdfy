from uuid import uuid4
from django.db import models


class Domain(models.Model):
    def __unicode__(self):
        return self.name

    name = models.URLField()


class DomainSearch(models.Model):
    uuid = models.CharField(max_length=36, default=lambda: uuid4())
    domain = models.ForeignKey(Domain)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)


class DomainSearchResult(models.Model):
    search_instance = models.ForeignKey(DomainSearch)
    result = models.TextField()
