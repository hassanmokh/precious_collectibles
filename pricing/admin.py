from typing import Any
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Pricing

@admin.register(Pricing)
class PricingModelAdmin(admin.ModelAdmin):
    list_display = ('type', 'local_buy', 'old')
    list_filter = ('type', 'old')
    
    fieldsets = (
        (None, {"fields": ("type",)}),
        (_("Price Local"), {"fields": ("local_buy", "local_sell")}),
        (_("Price World"), {"fields": ("world_buy", "world_sell")}),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),
        (_("Other Info"), {"fields": ("old",)})

    )
    
    def has_change_permission(self, *args, **kwargs):
        return False
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if change == False:
            Pricing.objects.filter(type=obj.type).update(old=True)
            
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.old = True
        obj.save()
    
    