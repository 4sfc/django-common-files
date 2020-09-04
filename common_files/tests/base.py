"""BaseAdminTest class"""

from unittest.mock import Mock

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.db import connection
from django.db import models
from django.db.utils import ProgrammingError
from django.test import TestCase
from django.test import RequestFactory

from common_files.admin.base import BaseAdmin
from common_files.models.base import Base


class BaseAdminTest(TestCase):
    """Test BaseAdmin"""

    @classmethod
    def setUpClass(cls):
        class BaseChild(Base):
            """Base child class test"""
            name = models.CharField(max_length=50)

            class Meta:
                app_label = 'common_files'

        @admin.register(BaseChild)
        class BaseChildAdmin(BaseAdmin):
            """Base child admin class test"""

        cls.model = BaseChild
        cls.model_admin = BaseChildAdmin

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.model)
            super().setUpClass()
        except ProgrammingError:
            pass

        request_factory = RequestFactory()
        cls.request = request_factory.get('/admin/common_files/base_child/')
        cls.request.user = User.objects.create(username='fb',
                                               email='f@example.com')

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.model)
            super().tearDownClass()
        except ProgrammingError:
            pass

    def test_save_model(self):
        """Test save_model"""
        model_admin = self.model_admin(self.model, AdminSite(self.model_admin))
        art = self.model(label='Art', value='AR', created_by=self.request.user,
                         modified_by=self.request.user)
        self.assertIsNone(art.id)
        model_admin.save_model(self.request, art, form=Mock(), change=False)
        self.assertEqual(self.model.objects.get(id=1).value, 'ar')
