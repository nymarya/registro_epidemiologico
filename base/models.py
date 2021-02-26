from django.db import models

# Create your models here.

class Estado(models.Model):
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
