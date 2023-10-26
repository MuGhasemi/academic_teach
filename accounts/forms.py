from django import forms
from .models import Student, User
from django.contrib.auth.forms import UserChangeForm
from django.forms import ImageField, FileInput


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

class EditStudentForm(forms.ModelForm):
    student_image= ImageField(widget=FileInput(attrs={
        'id':'profile-img',
    }))
    class Meta:
        model = Student
        fields = ('student_image',)
        widgets = {
            'profileImage': FileInput(attrs={
                'accept': '.jpg,.jpeg,.png,.PNG,.JPG,.JPEG',
                })}

class EditUserForm(UserChangeForm):
    class Meta():
        model = User
        fields =(
            'first_name',
            'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'disabled': 'disabled',
                                                'id': 'profileNameInput',}),
            'last_name': forms.TextInput(attrs={'disabled': 'disabled',
                                                'id': 'profileLastNameInput',}),}
    password = None


class StudentIncerateCreditForm(forms.Form):
    credit = forms.IntegerField(
        required = True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'مبلغ',
                'id':'priceToUp',
                'dir':'ltr',}))