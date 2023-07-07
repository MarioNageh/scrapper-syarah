from django.contrib import admin
from django.utils.safestring import mark_safe

from scrapper.models import Car


# Register your models here.

class CarAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)  # Add the field name of your image field here

    def image_tag(self, obj: Car):
        return mark_safe('<img src="%s" width="150" height="150" />' % obj.image_url)

    image_tag.short_description = 'Display Image'


admin.site.register(Car, CarAdmin)
