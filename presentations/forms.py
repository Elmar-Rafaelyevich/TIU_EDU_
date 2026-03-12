from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Group, Presentation

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input', 
        'placeholder': 'Пароль'
    }))

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Например: 9-А класс'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 3, 
                'placeholder': 'Описание группы (необязательно)'
            }),
        }

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Название презентации'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': '.pdf,.ppt,.pptx,.doc,.docx,.jpg,.jpeg,.png'
            }),
        }