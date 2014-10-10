from django import forms
from rango.models import Page,Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter the Category Name')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # an inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,help_text='Please enter the title of the page')
    url = forms.URLField(max_length=200,help_text='Please entre the url of the page')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        # We override the clean() method implemented in ModelForm
        # Code to verify and fix url field
        url = cleaned_data.get('url')
        #  if url is not empty and doesn't start with 'http://', prepend 'http://'
        if url and not url.startswith('http://'):
            url = 'http://'+ url
            cleaned_data['url'] = url
        return cleaned_data


    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

         # What fields do we want to include on the form?
         # This way we don't need every field in the model present.
         # Some fields may allow NULL values, so we may not want to include them...
         # Here, we are hiding the foreign key.
        fields =  ('title','url','views')


