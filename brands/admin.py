from django.contrib import admin
from brands.models import Brands


@admin.register(Brands)
class BrandAdminModel(admin.ModelAdmin):
    list_filter = ('name', 'is_deleted')
    list_display = ('name', 'is_deleted')
    search_fields = ('name',)
