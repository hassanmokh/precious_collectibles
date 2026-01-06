from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import Album, Photo


@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_deleted')
    list_filter = ('is_deleted',)
    
    fieldsets = (
        (_("Info."), {"fields": ("title", "description")}),
        (_("Info. Arabic"), {"fields": ("title_ar", "description_ar")}),
        (_("Actions"), {"fields": ("is_deleted",)}),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),

    )


@admin.register(Photo)
class PhotoModelAdmin(admin.ModelAdmin):
    list_display = ('album', 'created_at', 'is_deleted')
    list_filter = ('is_deleted',)
    
    fieldsets = (
        (_("Info."), {"fields": ("album",)}),
        (_("Path"), {"fields": ("url",)}),
        (_("Actions"), {"fields": ("is_deleted",)}),
        (_("Important dates"), {"fields": ("created_at", "updated_at")}),

    )
