from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import calcula_faixa_etaria

# Create your models here.

class UnidadeFederativa(models.Model):
    nome = models.CharField(u'Nome', max_length=80)
    sigla = models.CharField(u'Sigla', max_length=2)

    def __str__(self):
        return self.sigla


class Municipio(models.Model):
    codigo = models.CharField(u'Código IBGE', max_length=7, unique=True)
    nome = models.CharField(u'Nome', max_length=80)
    unidade_federativa = models.ForeignKey(UnidadeFederativa, on_delete=models.CASCADE)

    class Meta:
        ordering = ('nome', )

    def __str__(self):
        return u'%s / %s' % (self.nome, self.unidade_federativa.sigla)

    def get_sigla_estado(self):
        return u'%s / %s' % (self.nome, self.unidade_federativa.sigla)


class Doenca(models.Model):
    nome = models.CharField(max_length=80)
    cid = models.CharField(max_length=6, blank=True)

    class Meta:
        ordering = ('nome', )
        verbose_name = 'Doença'

    def __str__(self):
        cid_formatada = self.cid[:3] + '.' + self.cid[3:] if len(self.cid) > 3 else self.cid
        cid = u'(%s)' % cid_formatada if self.cid else ''
        return u'%s %s' % (self.nome, cid)


class PacienteDoenca(models.Model):
    paciente = models.ForeignKey('base.Paciente', on_delete=models.CASCADE)
    doenca = models.ForeignKey('base.Doenca', on_delete=models.CASCADE)
    tempo_diagnostico = models.CharField(u'Tempo de Diagnóstico', blank=True,
                                         max_length=100)

    class Meta:
        verbose_name = 'Doença do Paciente'
        verbose_name_plural = 'Doenças do Paciente'

    def __str__(self):
        return "Doença"


class Paciente(models.Model):
    usuario = models.OneToOneField('base.User', on_delete=models.CASCADE)
    descricao_caso = models.TextField(null=True)

    def __str__(self):
        return self.usuario.nome


class Medico(models.Model):
    usuario = models.OneToOneField('base.User', on_delete=models.CASCADE)
    crm = models.TextField('CRM', max_length=10)

    class Meta:
        verbose_name = 'Médico'

    def __str__(self):
        return self.usuario.nome

    @property
    def faixa_etaria(self):
        return calcula_faixa_etaria(self.usuario.data_nascimento)


class User(AbstractUser):
    SEXO_MASCULINO = u'M'
    SEXO_FEMININO = u'F'
    SEXO_NAO_INFORMADO = u'N'
    SEXO_CHOICES = (
        (SEXO_MASCULINO, u'Masculino'),
        (SEXO_FEMININO, u'Feminino'),
        (SEXO_NAO_INFORMADO, u'Não Informado')
    )
    SEXO_FORM_CHOICES = (
        ('', ''),
        (SEXO_MASCULINO, u'Masculino'),
        (SEXO_FEMININO, u'Feminino'),
    )

    nome = models.CharField(u'Nome', max_length=80)
    nome_mae = models.CharField(u'Nome da Mãe', max_length=80)
    cpf = models.CharField(u'CPF', max_length=15,
                           help_text=u'Digite o CPF sem pontos ou traços.',
                           null=True, unique=True)
    sexo = models.CharField(u'Sexo', max_length=1, choices=SEXO_CHOICES,
                            default=SEXO_NAO_INFORMADO)
    data_nascimento = models.DateField(u'Data de Nascimento', null=True)
    email = models.CharField(u'Email', max_length=80, null=True, blank=True)

    municipio = models.ForeignKey('base.Municipio', null=True, blank=True,
                                  on_delete=models.CASCADE)
    eh_gestor = models.BooleanField('É gestor',  default=False)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuário'

    def __str__(self):
        return self.nome
