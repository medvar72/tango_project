from __future__ import unicode_literals
from rango.models import Page,Category,UserProfile
from django.contrib.auth.models import User
from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import datetime
from django.contrib.admin import widgets
from django.utils import timezone


class CategoryForm(forms.ModelForm):
    name    = forms.CharField(max_length=128, help_text='Please enter the Category Name')
    views   = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes   = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug    = forms.CharField(widget=forms.HiddenInput(), required=False)

    # an inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text='Please enter the title of the page')
    url = forms.URLField(max_length=200,help_text='Please entre the url of the page')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    first_visit = forms.DateTimeField(widget=widgets.AdminSplitDateTime(), initial=timezone.now())
    last_visit = forms.DateTimeField(widget=widgets.AdminSplitDateTime(), initial=timezone.now())

    def clean(self):
        cleaned_data = self.cleaned_data
        # We override the clean() method implemented in ModelForm
        # Code to verify and fix url field
        url = cleaned_data.get('url')
        #  if url is not empty and doesn't start with 'http://', prepend 'http://'
        if url and not (url.startswith('http://') or url.startswith('https://')) :
            url = 'http://'+ url
            cleaned_data['url'] = url
        return cleaned_data

# Inline Class to specify fields to be showed
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

         # What fields do we want to include on the form?
         # This way we don't need every field in the model present.
         # Some fields may allow NULL values, so we may not want to include them...
         # Here, we are hiding the foreign key.
         # we can either exclude the category field from the form,
        # exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        fields =  ('title','url','views','first_visit','last_visit')

class UserForm(forms.ModelForm):
    """Form to define Users"""
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))
    # password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('website','picture')

class UserProfileForm(RegistrationForm):
    website = forms.URLField(max_length=200,help_text='Please entre the url of the page')
    picture = forms.ImageField()
    class Meta:
        model = UserProfile
        fields = '__all__'

    # def save(self, profile_callback=None):
    #     new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
    #     password=self.cleaned_data['password1'],
    #     email = self.cleaned_data['email'])
    #     new_profile = UserProfile(user=new_user, website=self.cleaned_data['website'], picture=self.cleaned_data['picture'])
    #     new_profile.save()
    #     return new_user
