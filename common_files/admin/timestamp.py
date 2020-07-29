'''TimestampAdmin class'''

from django.contrib import admin

class TimestampAdmin(admin.ModelAdmin):
    '''TimestampAdmin has custom save_formset and save_model functions'''

    def save_formset(self, request, form, formset, change):
        '''Save created_by and modified_by users.'''
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.pk is None:
                instance.created_by = request.user
            instance.modified_by = request.user
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        '''Save created_by and modified_by users.'''
        if obj.pk is None:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
