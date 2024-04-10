import re
from django import forms
from django.forms import ValidationError, widgets
from django.contrib.auth.models import User

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least:'
            '1 Uppercase letter,'
            '1 Lowercase letter,'
            '8 characters at minimu'
        ),
        code = 'Invalid'
    )

class Registerform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Type your username')
        add_attr(self.fields['email'], 'placeholder', 'Type your email')
        add_attr(self.fields['password'], 'placeholder', 'Type your password')
        add_attr(self.fields['password2'], 'placeholder', 'Retype your password')
        add_attr(self.fields['first_name'], 'placeholder', 'Your first name')
        add_attr(self.fields['last_name'], 'placeholder', 'Your last name')
    
    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 50 characters',
        },
        min_length=4, max_length=50,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        },
        validators=[strong_password],
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password'
        },
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Passwords do not match',
                code='invalid'
            )
            raise ValidationError({
                'password2': password_confirmation_error
            })