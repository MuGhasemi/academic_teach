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

class RegisterUserForm(forms.Form):
    username = forms.CharField(
        max_length = 30,
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'نام کاربری',
                'id':'sinUsername',}))
    first_name = forms.CharField(
        max_length = 20,
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'نام',
                'id':'sinFirstname',}))
    last_name = forms.CharField(
        max_length = 20,
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'نام خانوادگی',
                'id':'sinLastname',}))
    password = forms.CharField(
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'گذرواژه',
                'id':'sinPassword',}))
    confirm_password = forms.CharField(
        required = True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'تکرار گذرواژه',
                'id':'sinPasswordRep',}))
    email = forms.CharField(
        required = True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'ایمیل',
                'id':'sinEmail',}))