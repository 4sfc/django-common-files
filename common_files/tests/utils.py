"""CommonFilesUtilsTest class"""

from django.contrib.auth.models import User
from django.db import connection
from django.db import models
from django.db.utils import ProgrammingError
from django.test import TestCase

from common_files.models.base import Base
from common_files.models.timestamp import Timestamp
from common_files.utils import CommonFilesUtils


class CommonFilesUtilsTest(TestCase):
    """Tests CommonFilesUtils class"""

    @classmethod
    def setUpClass(cls):
        """Set up child classes"""

        class WithActive(Base):
            """Base child"""

        class WithoutActive(Timestamp):
            """Timestamp child"""
            label = models.CharField(max_length=191, unique=True)
            value = models.CharField(max_length=10, unique=True)

            def __str__(self):
                return '{}'.format(self.label)

            class Meta:
                app_label = 'common_files'

        cls.withactive = WithActive
        cls.withoutactive = WithoutActive

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.withactive)
                editor.create_model(cls.withoutactive)
            super().setUpClass()
        except ProgrammingError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.withactive)
                editor.delete_model(cls.withoutactive)
            super().tearDownClass()
        except ProgrammingError:
            pass

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='fbar', email='fb@example.com')
        cls.withactive.objects.bulk_create([
            cls.withactive(label='Art', value='a', active=True,
                           created_by=cls.user, modified_by=cls.user),
            cls.withactive(label='History', value='h', active=False,
                           created_by=cls.user, modified_by=cls.user),
            cls.withactive(label='Math', value='m', active=False,
                           created_by=cls.user, modified_by=cls.user),
            cls.withactive(label='Science', value='s', active=True,
                           created_by=cls.user, modified_by=cls.user)
        ])
        cls.withoutactive.objects.bulk_create([
            cls.withoutactive(label='Art', value='a',
                              created_by=cls.user, modified_by=cls.user),
            cls.withoutactive(label='History', value='h',
                              created_by=cls.user, modified_by=cls.user),
            cls.withoutactive(label='Math', value='m',
                              created_by=cls.user, modified_by=cls.user),
            cls.withoutactive(label='Science', value='s',
                              created_by=cls.user, modified_by=cls.user)
        ])

    def test_get_active_queryset_with_active_field(self):
        """Test get_active_queryset with a model having an active field"""
        qs = CommonFilesUtils.get_active_queryset('common_files',
                                                  self.withactive.__name__)
        expected_list = ['<WithActive: Art>', '<WithActive: Science>']
        self.assertQuerysetEqual(qs.order_by('id'), expected_list)

    def test_get_active_queryset_without_active_field(self):
        """Test get_active_queryset with a model having an active field"""
        qs = CommonFilesUtils.get_active_queryset('common_files',
                                                  self.withoutactive.__name__)
        expected_list = ['<WithoutActive: Art>', '<WithoutActive: History>',
                         '<WithoutActive: Math>', '<WithoutActive: Science>']
        self.assertQuerysetEqual(qs.order_by('id'), expected_list)
