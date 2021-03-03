from django import forms
from django_select2.forms import ModelSelect2Widget, Select2Widget
from localflavor.br.forms import BRCPFField

from base.models import User, Municipio


class PacienteForm(forms.ModelForm):
    cpf = BRCPFField(label=u'CPF', widget=forms.TextInput(
        attrs={'placeholder': '00.000.000-00', 'class': "form-control",
               'data-toggle': "input-mask",
               'data-mask-format': "000.000.000-00"}))
    nome = forms.CharField(label='Nome Completo', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo', 'class': "form-control"}))

    data_nascimento = forms.DateField(label=u'Data de Nascimento',
                                      widget=forms.DateInput(format='%d/%m/%Y',
                                                             attrs={
                                                                 'placeholder': 'dia/mês/ano',
                                                                 'class': 'form-control',
                                                                 'data-toggle': "input-mask",
                                                                 'data-mask-format': "00/00/0000",
                                                                 'data-parsley-pattern': "(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"}))

    sexo = forms.ChoiceField(label='Sexo',
                             choices=User.SEXO_FORM_CHOICES,
                             widget=Select2Widget(
                                 attrs={'class': "form-control",
                                        'data-placeholder': 'Selecione o sexo'}))
    municipio = forms.ModelChoiceField(label='Município',
                                       queryset=Municipio.objects,
                                       required=True,
                                       widget=ModelSelect2Widget(
                                           model=Municipio,
                                           search_fields=['nome__icontains'],
                                           attrs={'class': "form-control",
                                                  "data-minimum-input-length": "0",
                                                  "data-placeholder": "Busque e selecione um município"}))
    password = forms.CharField(
            label=u'Senha*',
            widget=forms.PasswordInput(render_value=False,
                                       attrs={'class': "form-control"})
        )

    confirma_password = forms.CharField(
        label=u'Confirmar Senha*',
        widget=forms.PasswordInput(render_value=False,
                                   attrs={'class': "form-control"})
    )

    class Meta:
        fields = ['email']
        model = User

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['email'].label = u'Email*'



    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get('confirma_password'):
            if self.cleaned_data.get('password') != self.cleaned_data.get('confirma_password'):
                self.add_error('password', u'As senhas não são iguais.')

        return self.cleaned_data
