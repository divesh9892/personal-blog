from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Category, User, Profile
from ckeditor_uploader.fields import RichTextUploadingField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ('slug',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'metaTitle': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'slug': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            # 'thumbnail': forms.ImageField(
            #     attrs={
            #         'class': 'form-control',
            #     }
            # ),
            'summary': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'tags': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'data-role': 'tagsinput'
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ('slug', 'postId')
        # widgets = {
        #     'category': forms.ModelChoiceField(
        #         attrs={
        #             'class': 'form-control'
        #         }
        #     ),
        # }


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'profileImg')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
