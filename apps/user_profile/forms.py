from django import forms
from user_profile.models import UserProfile


class ProfileForm(forms.ModelForm):
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        max_length=200
    )
    
    class Meta:
        model = UserProfile
        fields = ['foto', 'ocupacao', 'genero', 'telefone',
        'cidade','estado', 'descricao']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.CheckboxInput, forms.RadioSelect]:
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'