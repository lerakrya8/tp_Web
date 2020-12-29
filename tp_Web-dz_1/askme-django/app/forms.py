from django import forms
from django.forms import TextInput
from .models import *
import re
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
    }))


class Registration(forms.Form):
    login = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    repeat_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        if username.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password.strip() == '':
            raise forms.ValidationError('Password is empty', code='validation_error')
        if ' ' in password:
            raise forms.ValidationError('Password contains space.', code='space in password')

        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.strip() == '':
            raise forms.ValidationError('Username is empty', code='validation_error')
        if ' ' in email:
            raise forms.ValidationError('Email contains space.', code='space in email')

        return email

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        r_password = cleaned_data.get('repeat_password')

        if password != r_password:
            raise forms.ValidationError('These passwords do not match.')

    def save(self):
        new_user = User(username=self.cleaned_data.get('username'),
                        email=self.cleaned_data.get('email'),
                        password=self.cleaned_data.get('password'))
        new_user.set_password(self.cleaned_data.get('password'))
        username = self.clean_username()
        password = self.clean_password()
        profile = UserProfile(user=new_user, nickname=username)
        new_user.save()
        profile.save()
        return new_user, profile

class SettingsForm(forms.Form):
    user_login = forms.CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    login = forms.CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    email = forms.EmailField(required=False, widget=TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    username = forms.CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg',
    }), required=False)

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = ""

    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #     return avatar

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=True, widget=TextInput(attrs={
        'class': 'form-control form-control-lg',
    }))

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '7',
            }),
        }

        labels = {
            'title': 'Title',
            'text': 'Text',
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ""
        self.fields['text'].label = ""
        self.fields['tags'].label = ""

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        pattern = re.compile(r" |,")
        tags_ = pattern.split(tags)
        tags_set = list()
        for tag_name in tags_:
            tag = Tag.objects.filter(tag_title=tag_name).first()
            if tag is not None:
                tags_set.append(tag)
            else:
                tag = Tag.objects.create(tag_title=tag_name)
                tags_set.append(tag)
        print(len(tags_set))
        return tags_set

class AnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""

    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
        }

class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image_profile']
        required = None

    def __init__(self, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.fields['image_profile'].label = ""



