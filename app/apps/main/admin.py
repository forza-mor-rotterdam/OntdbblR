from apps.main.models import Regel
from django.contrib import admin
from django.contrib.admin import AdminSite

AdminSite.site_title = "OntdbblR Admin"
AdminSite.site_header = "OntdbblR Admin"
AdminSite.index_title = "OntdbblR Admin"


class RegelAdmin(admin.ModelAdmin):
    list_display = ("__str__", "deduplicate", "distance", "max_age", "onderwerp_url")
    list_editable = ("deduplicate", "distance", "max_age")


admin.site.register(Regel, RegelAdmin)
