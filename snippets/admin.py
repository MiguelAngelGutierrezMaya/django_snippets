from django.contrib import admin

from snippets.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Language admin."""

    list_display = ('pk', 'name', 'slug',)
    list_display_links = ('pk', 'name',)
    list_editable = ('slug',)

    search_fields = (
        'name',
        'slug'
    )

    list_filter = (
        'name',
        'slug',
    )
