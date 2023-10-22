from django import forms
from .models import Lesson

class SearchBoxForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id':'searchBox',
                'placeholder':'جستوجو',}),
        max_length=100,
        required = False,)

class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            'title',
            'description',
            'teacher',
            'registration_start',
            'registration_deadline',
            'start_date',
            'price',
            'capacity',
            'number_of_sessions',
            'lesson_image',)
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'c-name',
                'type': 'text',
            }),
            'description': forms.Textarea(attrs={
                'id':'c-desc',
            }),
            'registration_start': forms.DateInput(attrs={
                'id':'reg-start-date'
            }),
            'registration_deadline': forms.DateInput(attrs={
                'id':'reg-end-date'
            }),
            'start_date': forms.DateInput(attrs={
                'id':'start-class-date'
            }),
            'price': forms.NumberInput(attrs={
                'id':'num-book',
            }),
            'capacity': forms.NumberInput(attrs={
                'id':'capacity',
            }),
            'number_of_sessions': forms.NumberInput(attrs={
                'id':'sessions',
            }),
            'lesson_image': forms.FileInput(attrs={
                'id': 'c-img',
                'accept': '.jpg,.jpeg,.png,.PNG,.JPG,.JPEG',
                'class':'add-Cou-img'
            })}

