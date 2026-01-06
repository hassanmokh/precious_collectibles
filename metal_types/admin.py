from django.contrib import admin

from metal_types.models import MetalTypes

@admin.register(MetalTypes)
class MetalTypesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo',)