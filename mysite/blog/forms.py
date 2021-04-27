from django import forms

# For more info:
# https://docs.djangoproject.com/en/3.0/ref/forms/fields/

class EmailPostForm(forms.form):
    name = forms.CharField(max_length=25) #  Renders HTML input-type "text"
    email = forms.EmailField() #  Renders HTML input type but will require valid email address.
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.TextArea) #  Widgets override the default HTML, i.e. here we swap from Input to TextArea.

