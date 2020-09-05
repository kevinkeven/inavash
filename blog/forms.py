from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class EmailPostShare(forms.Form):
    name = forms.CharField(max_length=30, label='Your name')
    email = forms.EmailField(label='Email Address')
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name': _('Your name'),
            'email': _('Email Address'),
            'body': _('Your Comment')
        }

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Here')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'inlineFormInputGroupUsername'
        self.helper.form_class = 'form-control'

class Feedback(forms.Form):
    name = forms.CharField(max_length=30, label='Your name')
    email = forms.EmailField(label='Email Address')
    subject = forms.CharField(max_length=180)
    message = forms.CharField(widget=forms.Textarea)