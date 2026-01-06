from django.contrib import admin
from .models import Charts


@admin.register(Charts)
class ChartAdminModel(admin.ModelAdmin):
    list_display = ('type', 'world_buy_price', 'world_sell_price', 'local_buy_price', 'local_sell_price', 'created_at')
    list_filter = ('type',)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
