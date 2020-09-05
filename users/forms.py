from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'username',
                  'email', 'age', 'image', 'cv', 'facebook',
                  'twitter', 'instagram', 'linkdin',
                  'password1', 'password2',
        )
        labels = {
            'facebook': _('Facebook_URL'),
            'twitter': _('Twitter_URL'),
            'instagram': _('Instagram_URL'),
            'linkdin': _('Linkdin_URL')
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models = CustomUser
        fields = ('first_name', 'last_name', 'username',
                  'email', 'age', 'image', 'cv',
                  'facebook', 'twitter', 'instagram',
                  'linkdin',
        )
        labels = {
            'facebook': _('Facebook_URL'),
            'twitter': _('Twitter_URL'),
            'instagram': _('Instagram_URL'),
            'linkdin': _('Linkdin_URL')
        }
