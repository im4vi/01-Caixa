# features/admin.py

from django.contrib import admin
from .models import FeatureFlag

@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'enabled')
    list_filter = ('enabled',)
    search_fields = ('name',)
    list_editable = ('enabled',)
