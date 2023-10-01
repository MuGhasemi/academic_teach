from django import forms


class LoginUserForm(forms.Form):
    email = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'ایمیل',
                'id':'userName',
                'type':'email',}))
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'رمز ورود',
                'id':'password',}))
