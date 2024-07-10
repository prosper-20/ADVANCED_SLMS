from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Enrollment, Broadcast

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







