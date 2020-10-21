"""TimestampCreateViewTest"""

from django.contrib.auth.models import AnonymousUser, User
from django.db import connection, models
from django.db.utils import ProgrammingError
from django.test import RequestFactory, TestCase

from common_files.models.timestamp import Timestamp
from common_files.views.timestamp import TimestampCreateView


class TimestampCreateViewTest(TestCase):
    """TimestampCreateViewTest tests timestamp set at validation"""

    @classmethod
    def setUpClass(cls):
        class TimestampChild(Timestamp):
            """Test model"""
            name = models.CharField(max_length=100)

            def __str__(self):
                return self.name

            class Meta:
                app_label = 'common_files'

        class TimestampChildView(TimestampCreateView):
            """Test view"""

            model = TimestampChild
            fields = ['name']
            success_url = '/success'

        cls.model = TimestampChild
        cls.view = TimestampChildView
        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.model)
            super().setUpClass()
        except ProgrammingError:
            pass

        request_factory = RequestFactory()
        cls.request = request_factory.get('/common_files/view/timestampchild')

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.model)
            super().tearDownClass()
        except ProgrammingError:
            pass

    def test_form_valid_with_anonymous_user(self):
        """Test form_valid has request with anonymous user"""
        self.request.user = AnonymousUser()
        view_i = self.view(**{'request': self.request})
        modelform = view_i.get_form_class()
        form = modelform(data={'name': 'testing'})
        http_request = view_i.form_valid(form)
        self.assertEqual(http_request.url, '/success')
        self.assertIsNone(form.instance.modified_by)
        self.assertIsNone(form.instance.created_by)
        self.assertIsNotNone(form.instance.modified)
        self.assertIsNotNone(form.instance.created)

    def test_form_valid_with_known_user(self):
        """Test form_valid has request with known user"""
        self.request.user = User.objects.create(username='fb',
                                                email='fb@example.com')
        view_i = self.view(**{'request': self.request})
        modelform = view_i.get_form_class()
        form = modelform(data={'name': 'testing'})
        http_request = view_i.form_valid(form)
        self.assertEqual(http_request.url, '/success')
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.modified_by, self.request.user)
        self.assertEqual(form.instance.created_by, self.request.user)
        self.assertIsNotNone(form.instance.modified)
        self.assertIsNotNone(form.instance.created)
