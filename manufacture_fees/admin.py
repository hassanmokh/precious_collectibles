from django.contrib import admin
from .models import *

@admin.register(ManufactureFees)
class ManufactureFeesModelAdmin(admin.ModelAdmin):
    raw_id_fields = ('type',)