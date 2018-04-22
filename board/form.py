from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Category


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control'})
        }

class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']



def email_duplicate_check(email):
    try:
        User._default_manager.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError(
        '同じメールアドレスが既に登録済みです。'
    )


class SigninForm(UserCreationForm):
    username = forms.RegexField(
        max_length=15,
        min_length=4,
        regex=r'^[a-zA-Z][a-zA-Z0-9]+$',
        error_messages=dict(invalid='先頭を半角英字から始めて、4〜15文字の半角英数字で入力してください。')
    )

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2", "first_name", "last_name"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password (Repeat)'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'


    def clean_email(self):
        email = self.cleaned_data['email']
        return email_duplicate_check(email)


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
