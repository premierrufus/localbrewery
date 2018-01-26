from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Beer)
admin.site.register(Gyle)
admin.site.register(BrewingEvent)
admin.site.register(PackagingEvent)
admin.site.register(PackagingFormat)
