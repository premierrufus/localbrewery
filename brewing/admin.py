from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Batch)
admin.site.register(Beer)
admin.site.register(Equipment)
admin.site.register(Fermentable)
admin.site.register(Hop)
admin.site.register(Salt)
admin.site.register(Misc)
admin.site.register(Yeast)
admin.site.register(Style)
admin.site.register(Recipe)
admin.site.register(RecipeOption)


@admin.register(BrewingEvent)
class BrewingEventAdmin(admin.ModelAdmin):
	list_display = ('brew_date', 'brewer', 'vessel', 'recipe', 'get_batches' )




