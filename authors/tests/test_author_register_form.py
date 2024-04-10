from django.test import TestCase
from authors.forms import Registerform
from parameterized import parameterized

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username')
        ('email', 'Type your email')
        ('first_name', 'ex.: Lebron')
        ('last_name', 'ex.: Raymond James')
        ('password', 'Type your password')
        ('password2', 'Retype your password')
    ])

    def test_fields_placeholder(self, field, placeholder):
        form = Registerform()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Username')
        ('email', 'Email')
        ('first_name', 'First name')
        ('last_name', 'Last name')
        ('password', 'Password')
        ('password2', 'Password2')
    ])

    def test_fields_label(self, field, needed):
        form = Registerform()
        current = form[field].field.label
        self.assertEqual(current, needed)
    