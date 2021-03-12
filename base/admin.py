import json
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, F, CharField
from django.db.models.expressions import RawSQL, When, Case, Value

from . import utils
from .forms import PacienteAdminForm, MedicoAdminForm, UsuarioAdminForm
from .models import Medico, Paciente, User, PacienteDoenca, Doenca


# Register your models here.
class UsuarioAdmin(admin.ModelAdmin):
    model = User
    form = UsuarioAdminForm

    def save_model(self, request, obj, form, change):
        cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
        usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
        utils.salva_usuario(usuario, form, cpf)


class DoencaAdmin(admin.ModelAdmin):
    model = Doenca

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False


class MedicoAdmin(admin.ModelAdmin):
    form = MedicoAdminForm
    model = Medico

    list_display = ('medico', 'crm')
    search_fields = ['medico__nome__icontains']

    def medico(self, obj):
        return obj

    def crm(self, obj):
        return obj.crm

    def save_model(self, request, obj, form, change):
        cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
        usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
        utils.salva_usuario(usuario, form, cpf)
        obj.user = usuario
        obj.crm = form.cleaned_data['crm']
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(MedicoAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.request = request
            form.base_fields['nome'].initial = obj.user.nome
            form.base_fields['cpf'].initial = obj.user.cpf
            form.base_fields['nome_mae'].initial = obj.user.nome_mae
            data = obj.user.data_nascimento.strftime("%d/%m/%Y")
            form.base_fields['data_nascimento'].initial = data
            form.base_fields['sexo'].initial = obj.user.sexo
            form.base_fields['municipio'].initial = [obj.user.municipio.id]
            form.base_fields['email'].initial = obj.user.email
            form.base_fields['eh_gestor'].initial = obj.user.eh_gestor

            form.base_fields['password'].required = False
            form.base_fields['confirma_password'].required = False
        else:
            for field in form.base_fields.keys():
                form.base_fields[field].initial = None
            form.base_fields['password'].required = True
            form.base_fields['confirma_password'].required = True

        return form

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False

    def has_view_or_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.eh_gestor
        else:
            return False


class PacienteDoencaAdmin(admin.ModelAdmin):
    model = PacienteDoenca
    list_display = ('doenca', 'paciente', 'tempo_diagnostico')
    search_fields = ['doenca__nome__icontains', 'paciente__usuario__nome',
                     'tempo_diagnostico']

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or eh_medico
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or eh_medico
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or eh_medico
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or eh_medico or request.user.eh_gestor
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or eh_medico
        else:
            return False

    def has_view_or_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or eh_medico
        else:
            return False


class PacienteDoencaInline(admin.TabularInline):
    model = PacienteDoenca


class PacienteAdmin(admin.ModelAdmin):
    form = PacienteAdminForm
    inlines = [PacienteDoencaInline]

    model = Paciente

    list_display = ('nome', 'faixa_etaria')

    def nome(self, obj):
        return obj.usuario

    def faixa_etaria(self, obj):
        return utils.calcula_faixa_etaria(obj.usuario.data_nascimento)

    def save_model(self, request, obj, form, change):
        cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
        usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
        utils.salva_usuario(usuario, form, cpf)
        obj.user = usuario
        obj.descricao_caso = form.cleaned_data['descricao_caso']
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super(PacienteAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            form.request = request
            form.base_fields['nome'].initial = obj.user.nome
            form.base_fields['cpf'].initial = obj.user.cpf
            form.base_fields['nome_mae'].initial = obj.user.nome_mae
            data = obj.user.data_nascimento.strftime("%d/%m/%Y")
            form.base_fields['data_nascimento'].initial = data
            form.base_fields['sexo'].initial = obj.user.sexo
            form.base_fields['municipio'].initial = [obj.user.municipio.id]
            form.base_fields['email'].initial = obj.user.email

            form.base_fields['password'].required = False
            form.base_fields['confirma_password'].required = False
        else:
            for field in form.base_fields.keys():
                form.base_fields[field].initial = None
            form.base_fields['password'].required = True
            form.base_fields['confirma_password'].required = True

        return form

    def has_add_permission(self, request):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or request.user.eh_gestor or eh_medico
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or request.user.eh_gestor or eh_medico
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or request.user.eh_gestor or eh_medico
        else:
            return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or request.user.eh_gestor or eh_medico
        else:
            return False

    def has_module_permission(self, request):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or request.user.eh_gestor or eh_medico
        else:
            return False

    def has_view_or_change_permission(self, request, obj=None):
        if request.user.is_authenticated:
            eh_medico = Medico.objects.filter(usuario=request.user).exists()
            return request.user.is_superuser or request.user.eh_gestor or eh_medico
        else:
            return False


class MyAdminSite(AdminSite):
    site_header = 'Interface administrativa'

    def index(self, request, extra_context=None):
        doencas_pizza = Doenca.objects.annotate(y=Count('pacientedoenca'))\
            .filter(y__gt=0).extra(select={'name': 'nome'}).values('name', 'y')
        doencas_barra = Doenca.objects.values('nome',
                                              'pacientedoenca__paciente__usuario__municipio__unidade_federativa__sigla')\
            .annotate(y=Count('pacientedoenca'))\
            .annotate(uf=Count('pacientedoenca__paciente__usuario__municipio__unidade_federativa__sigla') )\
            .filter(y__gt=0).extra(select={'sigla': 'pacientedoenca__paciente__usuario__municipio__unidade_federativa__sigla'})\
            .values('nome', 'uf', 'y', sigla=F('pacientedoenca__paciente__usuario__municipio__unidade_federativa__sigla'))

        ufs = list(set([doenca['sigla'] for doenca in doencas_barra]))
        doencas = [{"name": doenca['nome'], "data": [doenca['uf'] if doenca['sigla'] == uf else 0 for uf in ufs]} for doenca in doencas_barra]

        classes = ['0-18', '19-25', '26-35', '36-50', '51-60', '61-70',
                   '71-80', '81-100']
        doencas_faixa = Doenca.objects.annotate(faixa=Case(
                     When(pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=0),
                          pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=18),
                          then=Value('0-18')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=19),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=25),
                then=Value('19-25')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=26),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=35),
                then=Value('26-35')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=36),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=50),
                then=Value('36-50')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=51),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=60),
                then=Value('51-60')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=61),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=70),
                then=Value('61-70')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=71),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=80),
                then=Value('71-80')),
            When(
                pacientedoenca__paciente__usuario__data_nascimento__lte=date.today() - relativedelta(years=81),
                pacientedoenca__paciente__usuario__data_nascimento__gte=date.today() - relativedelta(years=100),
                then=Value('81-100')),
            default=Value('>100'),
            output_field=CharField()
        )).annotate(y=Count('pacientedoenca')) \
        .annotate(faixa_n=Count('faixa'))\
        .filter(y__gt=0).values('nome', 'y', 'faixa_n', 'faixa')

        doencas2 = [{"type":"area","name": doenca['nome'], "data": [doenca['y'] if doenca['faixa'] == c else 0 for c in classes] } for doenca in doencas_faixa ]
        extra = {'pizza': json.dumps(list(doencas_pizza)),
                 'barra': {'ufs': json.dumps(ufs), 'series': json.dumps(doencas)},
                 'radar': json.dumps(doencas2)
                 }
        return super(MyAdminSite, self).index(request, extra_context=extra)


admin.site = MyAdminSite()

admin.site.register(User, UsuarioAdmin )
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(PacienteDoenca, PacienteDoencaAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Doenca, DoencaAdmin)
