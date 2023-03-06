from read_pdf.models import template, Fields, Jobs, Jobpdf
from django import forms

class templateFrom(forms.ModelForm):
    class Meta:
        model = template
        # fields = "__all__"
        exclude = ["author", "status"]

FieldFromSet = forms.modelformset_factory(Fields, exclude=["regex_type","regex"], extra=1)


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        # fields = "__all__"
        exclude = ["status",]
        # widgets = {"input": forms.ClearableFileInput(attrs={'multiple': True})}
        # exclude=["template",]

class FileModelForm(forms.ModelForm):
    class Meta:
        model = Jobpdf
        fields = ["input"]
        widgets = {
            'input': forms.ClearableFileInput(attrs={'multiple': True}),
        }
