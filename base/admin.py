from django.contrib import admin

from . import utils
from .forms import PacienteForm, PacienteAdminForm
from .models import Medico, Paciente, User


# Register your models here.


# class MedicoAdmin(admin.ModelAdmin):
#     fields = ['crm']

class MedicoInline(admin.TabularInline):
    model = Medico

# class DoencaInline(admin.StackedInline):
#     model = Choice
#     extra = 3


class PacienteInline(admin.TabularInline):
    model = Paciente


class UsuarioPacienteAdmin(admin.ModelAdmin):
    fields = ['cpf', 'nome', 'nome_mae', 'sexo', 'data_nascimento',
              'email', 'municipio', 'password']
    inlines = [PacienteInline]
    model = User

    class Meta:
        verbose_name = 'aa'


class UsuarioMedicoAdmin(admin.ModelAdmin):
    fields = ['cpf', 'nome', 'nome_mae', 'sexo', 'data_nascimento',
              'email', 'municipio', 'password']
    inlines = [MedicoInline]
    model = User


class PacienteAdmin(admin.ModelAdmin):
    form = PacienteAdminForm

    def save_model(self, request, obj, form, change):
        cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
        usuario = User.objects.get_or_create(username=cpf)[0]
        utils.save_user(usuario, form, cpf)
        obj.usuario = usuario
        obj.descricao_caso = form.cleaned_data['descricao_caso']
        obj.save()
        # if not change:
        #     frase = '{}{}'.format(obj.nome, user.username)
        #     senha = hashlib.sha1(frase.encode('utf-8')).hexdigest()[0:6]
        #     user.set_password(senha)
        #     user.save()
        #     enviar_email_cadastro(user, senha)

    def get_form(self, request, obj=None, **kwargs):
        form = super(PacienteAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.request = request
            form.base_fields['nome'].initial = obj.usuario.nome
            form.base_fields['cpf'].initial = obj.usuario.cpf
            form.base_fields['nome_mae'].initial = obj.usuario.nome_mae
            data = obj.usuario.data_nascimento.strftime("%d/%m/%Y")
            form.base_fields['data_nascimento'].initial = data
            form.base_fields['sexo'].initial = obj.usuario.sexo
            form.base_fields['municipio'].initial = [obj.usuario.municipio.id]
            form.base_fields['email'].initial = obj.usuario.email

            # todo: retirar senha no edit

        return form


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(User, UsuarioPacienteAdmin)
