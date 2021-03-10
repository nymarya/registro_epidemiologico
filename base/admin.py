from django.contrib import admin

from . import utils
from .forms import PacienteAdminForm, MedicoAdminForm
from .models import Medico, Paciente, User, PacienteDoenca, Doenca


# Register your models here.

class DoencaAdmin(admin.ModelAdmin):
    model = Doenca

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.eh_gestor

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor

    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.eh_gestor


class MedicoAdmin(admin.ModelAdmin):
    form = MedicoAdminForm

    def save_model(self, request, obj, form, change):
        cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
        usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
        utils.save_user(usuario, form, cpf)
        obj.usuario = usuario
        obj.crm = form.cleaned_data['crm']
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(MedicoAdmin, self).get_form(request, obj, **kwargs)
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
            form.base_fields['eh_gestor'].initial = obj.usuario.eh_gestor

            form.base_fields['password'].required = False
            form.base_fields['confirma_password'].required = False
        else:
            for field in form.base_fields.keys():
                form.base_fields[field].initial = None
            form.base_fields['password'].required = True
            form.base_fields['confirma_password'].required = True

        return form

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.eh_gestor

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor

    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.eh_gestor

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.eh_gestor


class PacienteDoencaAdmin(admin.ModelAdmin):
    model = PacienteDoenca
    list_display = ('doenca', 'paciente', 'tempo_diagnostico')
    search_fields = ['doenca__nome__icontains', 'paciente__usuario__nome',
                     'tempo_diagnostico']

    def has_add_permission(self, request):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or eh_medico

    def has_change_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or eh_medico

    def has_delete_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or eh_medico

    def has_view_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or eh_medico

    def has_module_permission(self, request):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or eh_medico

    def has_view_or_change_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or eh_medico


class PacienteDoencaInline(admin.TabularInline):
    model = PacienteDoenca


class PacienteAdmin(admin.ModelAdmin):
    form = PacienteAdminForm
    inlines = [PacienteDoencaInline]

    def save_model(self, request, obj, form, change):
        cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
        usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
        utils.save_user(usuario, form, cpf)
        obj.usuario = usuario
        obj.descricao_caso = form.cleaned_data['descricao_caso']
        obj.save()

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

            form.base_fields['password'].required = False
            form.base_fields['confirma_password'].required = False
        else:
            for field in form.base_fields.keys():
                form.base_fields[field].initial = None
            form.base_fields['password'].required = True
            form.base_fields['confirma_password'].required = True

        return form

    def has_add_permission(self, request):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or request.user.eh_gestor or eh_medico

    def has_change_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or request.user.eh_gestor or eh_medico

    def has_delete_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or request.user.eh_gestor or eh_medico

    def has_view_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or request.user.eh_gestor or eh_medico

    def has_module_permission(self, request):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or request.user.eh_gestor or eh_medico

    def has_view_or_change_permission(self, request, obj=None):
        eh_medico = Medico.objects.filter(usuario=request.user).exists()
        return request.user.is_superuser or request.user.eh_gestor or eh_medico


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(PacienteDoenca, PacienteDoencaAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Doenca, DoencaAdmin)
