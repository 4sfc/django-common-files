"""ActiveTabularInlineTest class"""

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.db import connection
from django.db import models
from django.db.utils import ProgrammingError
from django.test import TestCase
from django.test import RequestFactory

from common_files.admin.active_tabular_inline import ActiveTabularInline
from common_files.models.base import Base


class ActiveTabularInlineTest(TestCase):
    """Test ActiveTabularInline"""

    @classmethod
    def setUpClass(cls):
        class Department(models.Model):
            """Test model"""
            name = models.CharField(max_length=100)

            def __str__(self):
                return self.name

            class Meta:
                app_label = 'common_files'

        class Course(Base):
            """Base child"""

            class Meta:
                app_label = 'common_files'

        class DepartmentCourse(models.Model):
            """Model with foreign keys to a test model and base child"""
            department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                           related_name='+')
            course = models.ForeignKey(Course, on_delete=models.CASCADE,
                                       related_name='+')

            class Meta:
                app_label = 'common_files'

        class Instructor(models.Model):
            """Test model"""
            name = models.CharField(max_length=100)

            def __str__(self):
                return self.name

            class Meta:
                app_label = 'common_files'

        class DepartmentInstructor(models.Model):
            """Model with foreign keys to two regular models"""
            department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                           related_name='+')
            instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,
                                           related_name='+')

            class Meta:
                app_label = 'common_files'

        class DepartmentCourseInline(ActiveTabularInline):
            """Admin class with a test model and base child"""
            model = DepartmentCourse
            fk_name = 'department'

        class DepartmentInstructorInline(ActiveTabularInline):
            """Admin class to regular models"""
            model = DepartmentInstructor
            fk_name = 'department'

        cls.dept = Department
        cls.course = Course
        cls.inst = Instructor
        cls.dept_course = DepartmentCourse
        cls.dept_inst = DepartmentInstructor
        cls.dc_inline = DepartmentCourseInline
        cls.di_inline = DepartmentInstructorInline

        try:
            with connection.schema_editor() as editor:
                editor.create_model(cls.dept)
                editor.create_model(cls.inst)
                editor.create_model(cls.course)
                editor.create_model(cls.dept_inst)
                editor.create_model(cls.dept_course)
            super().setUpClass()
        except ProgrammingError:
            pass

    @classmethod
    def setUpTestData(cls):
        request_factory = RequestFactory()
        cls.request = request_factory.get('/admin/common_files/department/')
        cls.user = User.objects.create(username='fbar', email='f@example.com')

        lib = cls.dept.objects.create(name='Liberal Arts')
        sci = cls.dept.objects.create(name='Science')

        inst_a = cls.inst.objects.create(name='Instructor a')
        inst_b = cls.inst.objects.create(name='Instructor b')

        cls.dept_inst.objects.bulk_create([
            cls.dept_inst(department=lib, instructor=inst_a),
            cls.dept_inst(department=sci, instructor=inst_b)
        ])

        ptg = cls.course.objects.create(label='Painting', value='pa',
                                        created_by=cls.user,
                                        modified_by=cls.user)
        eng = cls.course.objects.create(label='English', value='en',
                                        created_by=cls.user,
                                        modified_by=cls.user)
        cpp = cls.course.objects.create(label='C++', value='c', active=False,
                                        created_by=cls.user,
                                        modified_by=cls.user)
        dif = cls.course.objects.create(label='Differential Calculus',
                                        value='dc',
                                        created_by=cls.user,
                                        modified_by=cls.user)
        pot = cls.course.objects.create(label='Pottery', value='po',
                                        active=False,
                                        created_by=cls.user,
                                        modified_by=cls.user)

        cls.dept_course.objects.bulk_create([
            cls.dept_course(department=lib, course=ptg),
            cls.dept_course(department=lib, course=eng),
            cls.dept_course(department=sci, course=cpp),
            cls.dept_course(department=sci, course=dif),
            cls.dept_course(department=lib, course=pot),
        ])

    @classmethod
    def tearDownClass(cls):
        try:
            with connection.schema_editor() as editor:
                editor.delete_model(cls.dept_inst)
                editor.delete_model(cls.dept_course)
                editor.delete_model(cls.inst)
                editor.delete_model(cls.course)
                editor.delete_model(cls.dept)
            super().tearDownClass()
        except ProgrammingError:
            pass

    def test_formfield_for_foreignkey_with_active_field(self):
        """Test formfield_for_foreignkey with active elements"""
        dc_inline_i = self.dc_inline(self.dept_course,
                                     AdminSite(self.dc_inline))
        db_field = self.dept_course.course.field
        choice_f = dc_inline_i.formfield_for_foreignkey(db_field, self.request)
        self.assertEqual(list(choice_f.choices),
                         [('', '---------'), (1, 'Painting'), (2, 'English'),
                          (4, 'Differential Calculus')])

    def test_formfield_for_foreignkey_without_active_field(self):
        """Test formfield_for_foreignkey without active elements"""
        di_inline_i = self.di_inline(self.dept_inst, AdminSite(self.di_inline))
        db_field = self.dept_inst.instructor.field
        choice_f = di_inline_i.formfield_for_foreignkey(db_field, self.request)
        self.assertEqual(list(choice_f.choices),
                         [('', '---------'), (1, 'Instructor a'),
                          (2, 'Instructor b')])
