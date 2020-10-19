"""TimestampCreateView class"""

from django.utils import timezone
from django.views.generic.edit import CreateView


class TimestampCreateView(CreateView):
    """TimestampCreateView has custom form_valid to save the timestamp"""

    def form_valid(self, form):
        now = timezone.now()
        if form.instance.pk is None:
            if self.request.user.is_authenticated:
                form.instance.created_by = self.request.user
            form.instance.created = now
        if self.request.user.is_authenticated:
            form.instance.modified_by = self.request.user
        form.instance.modified = now
        return super().form_valid(form)
