"""TimestampActiveAdminTest class"""

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.db import connection
from django.db import models
from django.db.utils import ProgrammingError
from django.test import TestCase
from django.test import RequestFactory

from common_files.admin.timestamp_active import TimestampActiveAdmin
from common_files.models.base import Base
from common_files.models.timestamp import Timestamp


class TimestampActiveAdminTest(TestCase):
    """Test TimestampActiveAdmin"""

    @classmethod
    def setUpClass(cls):

        class Department(Timestamp):
            """Timestamp child test"""
            name = models.CharField(max_length=50)
            def __str__(self):
                return self.name
            class Meta:
                app_label = 'common_files'

        class Major(Base):
            """Base child test"""
            class Meta:
                app_label = 'common_files'

        class DepartmentMajor(models.Model):
            """Model with base child foreign key"""
            department = models.ForeignKey(Department,
                                           on_delete=models.CASCADE,
                                           related_name='+')
            major = models.ForeignKey(Major, on_delete=models.CASCADE,
                                      related_name='+')
            class Meta:
                app_label = 'common_files'

        @admin.register(DepartmentMajor)
        class DepartmentMajorAdmin(TimestampActiveAdmin):
            """Model admin for a model with a base child foreign key"""

        cls.dept = Department
        cls.major = Major
        cls.dept_major = DepartmentMajor
        cls.dept_major_admin = DepartmentMajorAdmin

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.major)
                editor.create_model(cls.dept)
                editor.create_model(cls.dept_major)
            super().setUpClass()
        except ProgrammingError:
            pass

        request_factory = RequestFactory()
        cls.request = request_factory.get('/admin/common_files/timestamp/')
        cls.dm_admin_i = cls.dept_major_admin(cls.dept_major,
                                              AdminSite(cls.dept_major_admin))

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.dept_major)
                editor.delete_model(cls.dept)
                editor.delete_model(cls.major)
            super().tearDownClass()
        except ProgrammingError:
            pass

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='fbar', email='f@example.com')
        cls.major.objects.bulk_create([
            cls.major(label='Art', value='ar', created_by=cls.user,
                      modified_by=cls.user),
            cls.major(label='Biology', value='bi', created_by=cls.user,
                      modified_by=cls.user),
            cls.major(label='Computer Science', value='cs', active=False,
                      created_by=cls.user, modified_by=cls.user),
            cls.major(label='Design', value='de',
                      created_by=cls.user, modified_by=cls.user),
            cls.major(label='Electrical Engineering', value='ee', active=False,
                      created_by=cls.user, modified_by=cls.user)
        ])

        cls.dept.objects.bulk_create([
            cls.dept(name='Art', created_by=cls.user, modified_by=cls.user),
            cls.dept(name='Liberal Arts', created_by=cls.user,
                     modified_by=cls.user),
            cls.dept(name='Science and Engineering', created_by=cls.user,
                     modified_by=cls.user)
        ])

    def test_formfield_for_foreignkey_with_active_field(self):
        """Test formfield_for_foreignkey with active elements"""
        db_field = self.dept_major.major.field
        choice_f = self.dm_admin_i.formfield_for_foreignkey(db_field,
                                                            self.request)
        self.assertEqual(list(choice_f.choices),
                         [('', '---------'), (1, 'Art'), (2, 'Biology'),
                          (4, 'Design')])

    def test_formfield_for_foreignkey_without_active_field(self):
        """Test formfield_for_foreignkey without active elements"""
        db_field = self.dept_major.department.field
        choice_f = self.dm_admin_i.formfield_for_foreignkey(db_field,
                                                            self.request)
        self.assertEqual(list(choice_f.choices),
                         [('', '---------'), (1, 'Art'), (2, 'Liberal Arts'),
                          (3, 'Science and Engineering')])
