"""TimestampAdminTest class"""

from unittest.mock import Mock

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.db import connection
from django.db import models
from django.db.utils import ProgrammingError
from django.forms import inlineformset_factory
from django.test import TestCase
from django.test import RequestFactory

from common_files.admin.timestamp import TimestampAdmin
from common_files.models.timestamp import Timestamp


class TimestampAdminTest(TestCase):
    """Test TimestampAdmin"""

    @classmethod
    def setUpClass(cls):
        class Parent(models.Model):
            """Parent class"""

        class TimestampChild(Timestamp):
            """Timestamp child class"""
            parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

            def __str__(self):
                return '{}'.format(self.id)

        @admin.register(TimestampChild)
        class TimestampChildAdmin(TimestampAdmin):
            """Timestamp child admin class"""

        cls.parent = Parent
        cls.model = TimestampChild
        cls.model_admin = TimestampChildAdmin

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.parent)
                editor.create_model(cls.model)
            super().setUpClass()
        except ProgrammingError:
            pass

        cls.user = User.objects.create(username='fb', email='fb@example.com')
        cls.admin = cls.model_admin(cls.model, AdminSite(cls.model_admin))
        request_factory = RequestFactory()
        cls.request = request_factory.get('/admin/common_files/timestamp/')
        cls.request.user = cls.user
        cls.parent_obj = cls.parent.objects.create()

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.model)
                editor.delete_model(cls.parent)
            super().tearDownClass()
        except ProgrammingError:
            pass

    def test_save_formset(self):
        """Test save_formset"""
        tsc_formset = inlineformset_factory(self.parent, self.model,
                                            exclude=['created', 'modified'])
        form_data = {'timestampchild_set-TOTAL_FORMS': 1,
                     'timestampchild_set-INITIAL_FORMS': 0,
                     'timestampchild_set-MAX_NUM_FORMS': '',
                     'timestampchild_set-0-parent': self.parent_obj.id,
                     'timestampchild_set-0-created_by': self.user.id,
                     'timestampchild_set-0-modified_by': self.user.id}
        formset = tsc_formset(data=form_data, instance=self.parent_obj)
        self.assertTrue(formset.is_valid())
        self.assertQuerysetEqual(self.model.objects.all(), [])
        self.admin.save_formset(self.request, Mock(), formset, False)
        self.assertQuerysetEqual(self.model.objects.all(),
                                 ['<TimestampChild: 1>'])

    def test_save_model(self):
        """Test save_model"""
        obj = self.model(parent=self.parent_obj, created_by=self.user,
                         modified_by=self.user)
        self.assertIsNone(obj.id)
        self.admin.save_model(self.request, obj, form=Mock(), change=False)
        self.assertIsNotNone(self.model.objects.get(created_by=self.user))
