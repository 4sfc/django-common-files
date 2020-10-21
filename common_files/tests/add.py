"""AddViewTest"""

from django.contrib.auth.models import AnonymousUser
from django.db import connection
from django.db.utils import ProgrammingError
from django.forms.models import modelformset_factory
from django.test import RequestFactory, TestCase
from django.utils import timezone

from common_files.models.base import Base
from common_files.views.add import AddView


class AddViewTest(TestCase):
    """AddViewTest tests AddView"""

    @classmethod
    def setUpClass(cls):
        class BaseChild(Base):
            """Base child"""

            def __str__(self):
                return self.value

            class Meta:
                app_label = 'common_files'

        cls.model = BaseChild

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.model)
            super().setUpClass()
        except ProgrammingError:
            pass

        class AddChildView(AddView):
            """AddView child"""
            form_class = modelformset_factory(BaseChild,
                                              fields=('label', 'value'))

        request_factory = RequestFactory()
        request = request_factory.get('/common_files/add')
        request.user = AnonymousUser()

        kwargs = {'request': request, 'success_url': '/success',
                  'template_name': 'common_files/add_form.html'}
        cls.view = AddChildView(**kwargs)

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.model)
            super().tearDownClass()
        except ProgrammingError:
            pass

    def test_constructor_has_objects(self):
        """Test constructor has an object list"""
        self.assertTrue(hasattr(self.view, 'object_list'))

    def test_form_valid(self):
        """Test form_valid saves form to object_list"""
        data = {'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-MIN_NUM_FORMS': '',
                'form-0-label': 'Option 1',
                'form-0-value': '1',
                'form-0-created': timezone.now(),
                'form-0-created_by': '',
                'form-0-modified': timezone.now(),
                'form-0-modified_by': '',
                'form-1-label': 'Option 2',
                'form-1-value': '2',
                'form-1-created': timezone.now(),
                'form-1-created_by': '',
                'form-1-modified': timezone.now(),
                'form-1-modified_by': ''}
        form_class = self.view.get_form_class()
        form = form_class(data=data)
        self.assertEqual(list(self.model.objects.all()), [])
        self.assertTrue(self.view.form_valid(form))
        self.assertEqual(str(list(self.model.objects.all())),
                         '[<BaseChild: 1>, <BaseChild: 2>]')
        self.assertEqual(str(list(self.view.object_list)),
                         '[<BaseChild: 1>, <BaseChild: 2>]')

    def test_get_context_data(self):
        """Test get_context_data adds form to kwargs"""
        kwargs = self.view.get_context_data()
        self.assertTrue(kwargs, 'form')
