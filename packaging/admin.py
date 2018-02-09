from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Format)
#admin.site.register(PackagingEvent)
admin.site.register(PackagedFormat)


@admin.register(PackagingEvent)
class PackagingEventAdmin(admin.ModelAdmin):
	list_display = ('packaging_date', 'brewing_event', 'packager', 'get_formats')