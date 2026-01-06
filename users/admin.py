from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from users.models import User


admin.site.site_title = "Precious Collectibles"
admin.site.index_title = "Precious Collectibles"
admin.site.site_header = "Precious Collectibles"

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ['last_login', 'date_joined', 'verification_code']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_deleted",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Verifications"), {"fields": ("is_email_verified","verification_code")}),

    )
