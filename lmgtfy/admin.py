from django.contrib import admin

from lmgtfy.models import TLD


class TLDAdmin(admin.ModelAdmin):
    pass


admin.site.register(TLD, TLDAdmin)
