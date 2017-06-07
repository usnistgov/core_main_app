""" Form needed for the user part of everything
"""
from django import forms


class LoginForm(forms.Form):
    """ Custom login form for the user
    """
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)

    next_page = forms.CharField(widget=forms.HiddenInput)
