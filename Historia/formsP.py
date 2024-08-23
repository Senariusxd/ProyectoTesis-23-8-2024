from django import forms
from .models import EGeneral

class EGeneralForm(forms.ModelForm):
    class Meta:
        model = EGeneral
        fields = [
            'descripcion',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            

