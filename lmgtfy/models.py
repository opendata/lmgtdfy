from uuid import uuid4
from django.db import models


class SearchedSite(models.Model):
    base_url = models.TextField()
    path = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class SearchResult(models.Model):
    uuid = models.CharField(max_length=36, default=lambda: uuid4())
    site = models.ForeignKey(SearchedSite)
    result = models.TextField()
