'''CommonFilesUtils class'''

from django.apps.registry import apps

class CommonFilesUtils:
    '''Helper functions for CommonFiles'''

    @staticmethod
    def get_active_queryset(app_label, model):
        '''Return queryset of active values'''
        queryset = None
        try:
            model = apps.get_model(app_label, model)
        except LookupError:
            model = None
        if model and model._meta.get_field('active'):
            queryset = model.objects.filter(active=True)
        return queryset
