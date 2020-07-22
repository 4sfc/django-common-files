'''BaseAdmin class'''

from common_files.admin.timestamp import TimestampAdmin

class BaseAdmin(TimestampAdmin):
    '''BaseAdmin has a custom save_model function'''

    def save_model(self, request, obj, form, change):
        obj.value = obj.value.lower()
        super().save_model(request, obj, form, change)
