# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

"""
Sobre organização de Código e PEP-8: utilizar o Python
classes, semanticamente organizadas
 > choices
 > models fields
 > class Meta
 > override methods (save, clean)
 > property
 > business methods
"""


class Base(models.Model):

    criado_em = models.DateTimeField('Criado em', auto_now_add=True, blank=False, null=False)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True

    def get_criado_em(self, format):
        return self.criado_em.__format__(format).__str__()

    def get_atualizado_em(self, format):
        return self.atualizado_em.__format__(format).__str__()


class Condominio(Base):

    cnpj = models.CharField('CNPJ', max_length=11, unique=True, blank=False, null=False)
    nome = models.CharField('Nome', max_length=100, blank=False, null=False)
    endereco = models.CharField('Endereco', max_length=200, blank=False, null=False)
    sindico = models.OneToOneField('Perfil', on_delete=models.SET_NULL, related_name='condominio_administrado', blank=True, null=True)

    class Meta:
        verbose_name = 'Condominio'
        verbose_name_plural = 'Condominios'
        ordering = ('nome', )
        unique_together = (('cnpj','nome'), )

    def __str__(self):
        return self.nome


class GrupoHabitacional(Base):

    TIPO_GRUPO_HABITACIONAL = (
        ('quadra', 'Quadra'),
        ('bloco', 'Bloco'),
        ('torre', 'Torre'),
    )

    TIPO_UNIDADE_HABITACIONAL = (
        ('apartamento', 'Apartamento'),
        ('casa', 'Casa'),
        ('chale', 'Chale'),
    )

    nome = models.CharField('Nome', max_length=64, blank=False, null=False)
    tipo = models.CharField('Tipo', max_length=64, choices=TIPO_GRUPO_HABITACIONAL, blank=False, null=False)
    tipo_unidade = models.CharField('Tipo unidade', max_length=64, choices=TIPO_UNIDADE_HABITACIONAL, blank=False, null=False)
    logradouro = models.CharField('Logradouro', max_length=256, blank=True, null=True)

    condominio = models.ForeignKey('Condominio', on_delete=models.CASCADE, related_name='grupos_habitacionais', blank=False, null=False,)

    class Meta:
        verbose_name = 'Grupo Habitacional'
        verbose_name_plural = 'Grupos Habitacionais'
        ordering = ('nome', )
        unique_together = (('nome', 'condominio'),)

    def __str__(self):
        return '%s - %s - %s' % (self.condominio, self.tipo, self.nome)


class UnidadeHabitacional(Base):

    nome = models.CharField(max_length=16, blank=False, null=False)
    grupo_habitacional = models.ForeignKey('GrupoHabitacional', on_delete=models.CASCADE, related_name='unidades_habitacionais', blank=False, null=False)
    proprietario = models.ForeignKey('Perfil', on_delete=models.SET_NULL, related_name='unidades_habitacionais', blank=True, null=True)

    class Meta:
        verbose_name = 'Unidade Habitacional'
        verbose_name_plural = 'Unidades Habitacionais'
        ordering = ('nome', )
        unique_together = (('nome', 'grupo_habitacional'),)

    # def moradores(self):
    #     grupo_moradores = " "
    #     for morador in self.moradores:
    #         grupo_moradores + morador + " "
    #
    #     return grupo_moradores

    def __str__(self):
        return "%s %s - %s %s" % (self.grupo_habitacional.tipo, self.grupo_habitacional.nome, self.grupo_habitacional.tipo_unidade, self.nome)


class Perfil(Base):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    sexo = models.CharField('Sexo', max_length=16, choices=SEXO_CHOICES, blank=False, null=False)
    telefone = models.CharField('Telefone', max_length=16, blank=False, null=False)
    data_nascimento = models.DateField('Data de nascimento', blank=False, null=False)

    portaria = models.BooleanField('Portaria', default=False, blank=False, null=False)
    unidade_habitacional = models.ForeignKey('UnidadeHabitacional', related_name= 'moradores', blank=True, null=True)
    usuario = models.OneToOneField(User, related_name='perfil')
    condominio = models.ForeignKey('Condominio', related_name='perfis', on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return "%s %s" % (self.nome(), self.sobrenome())

    def nome(self):
        return self.usuario.first_name

    def sobrenome(self):
        return self.usuario.last_name