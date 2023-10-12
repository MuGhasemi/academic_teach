from django import forms

class SearchBoxForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id':'searchBox',
                'placeholder':'جستوجو',}),
        max_length=100,
        required = False,)