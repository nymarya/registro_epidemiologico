from django import forms
from django.core.paginator import Paginator
from django_select2.forms import ModelSelect2Widget, Select2Widget, \
    ModelSelect2MultipleWidget
from localflavor.br.forms import BRCPFField

from base.models import User, Municipio, Doenca, Paciente, Medico


class PacienteForm(forms.ModelForm):
    cpf = BRCPFField(label=u'CPF', widget=forms.TextInput(
        attrs={'placeholder': '000.000.000-00', 'class': "form-control",
               'data-toggle': "input-mask",
               'data-mask-format': "000.000.000-00"}))
    nome = forms.CharField(label='Nome Completo', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo', 'class': "form-control"}))
    nome_mae = forms.CharField(label='Nome da Mãe', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo da mãe', 'class': "form-control"}))

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
                                        'data-placeholder': 'selecione o sexo'}))
    municipio = forms.ModelChoiceField(label='Município',
                                       queryset=Municipio.objects,
                                       required=True,
                                       widget=ModelSelect2Widget(
                                           model=Municipio,
                                           search_fields=['nome__icontains'],
                                           attrs={'class': "form-control",
                                                  "data-minimum-input-length": "0",
                                                  "data-placeholder": "busque e selecione um município"}))
    doencas = forms.ModelMultipleChoiceField(label='Doenças',
                                             queryset=Doenca.objects,
                                             required=False,
                                             widget=ModelSelect2MultipleWidget(
                                                 model=Doenca,
                                                 search_fields=[
                                                     'nome__icontains'],
                                                 attrs={'class': "form-control",
                                                        "data-minimum-input-length": "0",
                                                        "data-placeholder": "busque e selecione as doenças que possui"}))

    descricao_caso = forms.CharField(label=u'Descrição do caso',
                                     widget=forms.Textarea(
                                         attrs={
                                             'placeholder': 'descreva seu caso',
                                             'class': "form-control"}))
    email = forms.CharField(label=u'Email', required=True,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'email@email.com',
                                       'class': "form-control"}))
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
        fields = ['cpf']
        model = Paciente

    # def __init__(self, *args, **kwargs):
    #     super(PacienteForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['email'].required = True
    #     self.fields['email'].label = u'Email*'

    def clean(self):
        if self.cleaned_data.get('password') and self.cleaned_data.get(
                'confirma_password'):
            if self.cleaned_data.get('password') != self.cleaned_data.get(
                    'confirma_password'):
                self.add_error('password', u'As senhas não são iguais.')

        return self.cleaned_data


class PacienteAdminForm(forms.ModelForm):
    cpf = BRCPFField(label=u'CPF', widget=forms.TextInput(
        attrs={'placeholder': '000.000.000-00', 'class': "form-control",
               'data-toggle': "input-mask",
               'data-mask-format': "000.000.000-00"}))
    nome = forms.CharField(label='Nome Completo', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo', 'class': "form-control"}))
    nome_mae = forms.CharField(label='Nome da Mãe', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo da mãe', 'class': "form-control"}))

    data_nascimento = forms.DateField(label=u'Data de Nascimento',
                                      widget=forms.DateInput(format='%d/%m/%Y',
                                                             attrs={
                                                                 'placeholder': 'dia/mês/ano',
                                                                 'class': 'form-control',
                                                                 'data-toggle': "input-mask",
                                                                 'data-mask-format': "00/00/0000",
                                                                 'data-parsley-pattern': "(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"}))

    sexo = forms.ChoiceField(label='Sexo', choices=User.SEXO_FORM_CHOICES,
                             widget=forms.Select(
                                 attrs={'class': "form-control",
                                        'data-placeholder': 'selecione o sexo'}))
    # municipio = forms.ModelChoiceField(label='Município',
    #                                    queryset=Municipio.objects,
    #                                    required=True,
    #                                    widget=ModelSelect2Widget(
    #                                        model=Municipio,
    #                                        search_fields=['nome__icontains'],
    #                                        attrs={'class': "form-control django-select2",
    #                                               "data-minimum-input-length": "0",
    #                                               "data-placeholder": "busque e selecione um município"}))

    municipio = forms.ModelChoiceField(Municipio.objects,
                                       label=u'Município', required=True,
                                       empty_label=u'Selecione o Município',
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control django-select2'}
                                       ))

    descricao_caso = forms.CharField(label=u'Descrição do caso',
                                     widget=forms.Textarea(
                                         attrs={
                                             'placeholder': 'descreva seu caso',
                                             'class': "form-control"}))
    email = forms.CharField(label=u'Email', required=True,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'email@email.com',
                                       'class': "form-control"}))
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
        fields = ['cpf']
        model = Paciente


class MedicoAdminForm(forms.ModelForm):
    cpf = BRCPFField(label=u'CPF', widget=forms.TextInput(
        attrs={'placeholder': '000.000.000-00', 'class': "form-control",
               'data-toggle': "input-mask",
               'data-mask-format': "000.000.000-00"}))
    nome = forms.CharField(label='Nome Completo', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo', 'class': "form-control"}))
    nome_mae = forms.CharField(label='Nome da Mãe', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo da mãe', 'class': "form-control"}))

    data_nascimento = forms.DateField(label=u'Data de Nascimento',
                                      widget=forms.DateInput(format='%d/%m/%Y',
                                                             attrs={
                                                                 'placeholder': 'dia/mês/ano',
                                                                 'class': 'form-control',
                                                                 'data-toggle': "input-mask",
                                                                 'data-mask-format': "00/00/0000",
                                                                 'data-parsley-pattern': "(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"}))

    sexo = forms.ChoiceField(label='Sexo', choices=User.SEXO_FORM_CHOICES,
                             widget=forms.Select(
                                 attrs={'class': "form-control",
                                        'data-placeholder': 'selecione o sexo'}))
    municipio = forms.ModelChoiceField(Municipio.objects,
                                       label=u'Município', required=True,
                                       empty_label=u'Selecione o Município',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control django-select2'}
                                       ))

    crm = forms.CharField(label=u'CRM', widget=forms.TextInput(
                                         attrs={'placeholder': 'CRM',
                                                'class': "form-control"}))

    eh_gestor = forms.BooleanField(label=u'É gestor', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control'}
    ))
    email = forms.CharField(label=u'Email', required=True,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'email@email.com',
                                       'class': "form-control"}))
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
        fields = ['cpf']
        model = Medico

class UsuarioAdminForm(forms.ModelForm):
    cpf = BRCPFField(label=u'CPF', widget=forms.TextInput(
        attrs={'placeholder': '000.000.000-00', 'class': "form-control",
               'data-toggle': "input-mask",
               'data-mask-format': "000.000.000-00"}))
    nome = forms.CharField(label='Nome Completo', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo', 'class': "form-control"}))
    nome_mae = forms.CharField(label='Nome da Mãe', widget=forms.TextInput(
        attrs={'placeholder': 'nome completo da mãe', 'class': "form-control"}))

    data_nascimento = forms.DateField(label=u'Data de Nascimento',
                                      widget=forms.DateInput(format='%d/%m/%Y',
                                                             attrs={
                                                                 'placeholder': 'dia/mês/ano',
                                                                 'class': 'form-control',
                                                                 'data-toggle': "input-mask",
                                                                 'data-mask-format': "00/00/0000",
                                                                 'data-parsley-pattern': "(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"}))

    sexo = forms.ChoiceField(label='Sexo', choices=User.SEXO_FORM_CHOICES,
                             widget=forms.Select(
                                 attrs={'class': "form-control",
                                        'data-placeholder': 'selecione o sexo'}))
    municipio = forms.ModelChoiceField(Municipio.objects,
                                       label=u'Município', required=True,
                                       empty_label=u'Selecione o Município',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control '}
                                       ))

    email = forms.CharField(label=u'Email', required=True,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'email@email.com',
                                       'class': "form-control"}))
    eh_gestor = forms.BooleanField(label=u'É gestor', required=False,
                                   widget=forms.CheckboxInput(
                                       attrs={'class': 'form-control'}
                                   ))
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
        fields = ['cpf']
        model = User
