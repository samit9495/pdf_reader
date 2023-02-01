from read_pdf.models import template, Fields, Jobs
from django import forms


class templateFrom(forms.ModelForm):
    class Meta:
        model = template
        # fields = "__all__"
        exclude = ["author", "status"]

FieldFromSet = forms.modelformset_factory(Fields, fields="__all__", extra=1)


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = "__all__"
        # exclude=["template",]