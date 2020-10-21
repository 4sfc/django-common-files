"""AddView class"""

from django.views.generic.edit import FormView


class AddView(FormView):
    """AddView has an object and custom functions"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = None

    def form_valid(self, form):
        self.object_list = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs.update({'form': self.get_form()})
        return super().get_context_data(**kwargs)
