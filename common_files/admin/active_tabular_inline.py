"""ActiveTabularInline class"""

from django.contrib import admin

from common_files.utils import CommonFilesUtils as cfu


class ActiveTabularInline(admin.TabularInline):
    """ActiveTabularInline has custom formfield_for_foreignkey"""

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Display only active values"""
        queryset = cfu.get_active_queryset(self.model._meta.app_label,
                                           db_field.name)
        if queryset:
            kwargs['queryset'] = queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
