from tkinter.tix import Form

from django import forms

class AddForm(forms,Form):
    site = forms.CharField()