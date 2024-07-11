from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Enrollment, Broadcast
from .validator import validate_file_size


ModuleFormSet = inlineformset_factory(Course, Module,
fields=['title',
'description'],
extra=2,
can_delete=True)


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']


class BroadCastForm(forms.ModelForm):
    class Meta:
        model = Broadcast
        fields = ["course", "subject", "message"]

from .models import CourseMaterials

class CourseMaterialsForm(forms.ModelForm):
    class Meta:
        model = CourseMaterials
        fields = ['title', 'description', 'file']


    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            validate_file_size(file)
        return file








