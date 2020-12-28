from django import forms
from django.forms import TextInput
from .models import *
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    user_login = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
    }))

class Registration(forms.ModelForm):
    login = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control form-control-lg',
                               }),
                               label='Password check')
    repeat_password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control form-control-lg',
                               }),
                               label='Password check')
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean(self):
        if not 'password' in self.cleaned_data or not 'repeat_password' in self.cleaned_data:
            raise forms.ValidationError('Enter password!')
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            self.add_error('password', 'Passwords do not match!')
            # self.add_error('password2', 'Passwords do not match!')
            raise forms.ValidationError('Passwords do not match!')

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error(None, 'This username is already in use')
            raise forms.ValidationError('This username is already in use')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error(None, 'This email is already in use')
            raise forms.ValidationError('This email is already in use')
        return self.cleaned_data['email']

    def save(self, **kwargs):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username, email, password)

        UserProfile.objects.create(user=user, nickname=username)
        # avatar = self.cleaned_data['avatar']
        # if avatar is not None:
        #     Profile.avatar.set(avatar)

        return user

# class SettingsForm(form.Form):
#     user_login = forms.CharField(required=False, widget=TextInput(attrs={
#         'class': 'form-control form-control-lg',
#     }),
#     value='')



