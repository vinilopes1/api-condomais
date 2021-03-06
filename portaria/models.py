# coding: utf-8
from django.db import models
from comum.models import Base, Perfil, UnidadeHabitacional
from rest_framework.fields import ImageField


class Post(Base):

    TIPO_POST = (
        ('ocorrencia', 'Ocorrencia'),
        ('aviso', 'Aviso'),
        ('entrada', 'Entrada'),
    )

    tipo = models.CharField('Tipo', max_length=64, choices=TIPO_POST, blank=False, null=False)
    publico = models.BooleanField('Publico', default=False, blank=False, null=False)
    informante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='posts', blank=False, null=False)

    descricao = models.CharField('Descricao', max_length=256, blank=True, null=True)
    foto = models.ImageField(upload_to='imgs', default='imgs/none/no_image.png')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def atualizado_em_data_br(self):
        return self.get_atualizado_em("%d de %B ")

    def atualizado_em_hora_br(self):
        return self.get_atualizado_em("%H:%M")

    def status_post(self):
        return "Entrada %s" % self.entrada.status if self.tipo == "entrada" else "Ocorrência %s" % self.ocorrencia.status


class Ocorrencia(Post):

    STATUS_OCORRENCIA = (
        ('resolvido', 'Resolvido'),
        ('reaberta', 'Reaberta'),
        ('finalizada', 'Finalizada'),
        ('aberta', 'Aberta'),
        ('em_analise', 'Em Analise'),
    )

    status = models.CharField('Status', max_length=64, choices=STATUS_OCORRENCIA, default='aberta', blank=False, null=False)
    localizacao = models.CharField('Localizacao', max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = 'Ocorrência'
        verbose_name_plural = 'Ocorrências'

    def __str__(self):
        return '%s (%s)' % (self.descricao, self.informante)


class Comentario(Base):

    descricao = models.CharField('Descricao', max_length=256, blank=False, null=False)
    ocorrencia = models.ForeignKey('Ocorrencia', on_delete = models.CASCADE, related_name = 'comentarios', blank=False, null=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return self.descricao


class Entrada(Post):

    STATUS_ENTRADA = (
        ('informada', 'Informada'),
        ('lida', 'Lida'),
        ('liberada', 'Liberada'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
    )

    data = models.DateField('Data', blank=False, null=False)
    hora = models.TimeField('Hora', blank=True, null=True)
    status = models.CharField('Status', max_length=64, choices=STATUS_ENTRADA, default='informada', blank=False, null=False)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def hora_entrada(self):
        return self.get_atualizado_em("%Hh %Mmin")

    def data_entrada(self):
        return self.get_atualizado_em("%d de %B")

    def liberar_entrada(self):
        if self.status == 'informada':
            self.status = 'liberada'
            self.save()
            return "Entrada liberada"

        return "Não foi possivel liberar esta entrada"


    def finalizar_entrada(self):
        if self.status == 'liberada':
            self.status = 'atendida'
            self.save()
            return "Entrada finalizada"

        return "Não foi possivel finalizar esta entrada"

    def cancelar_entrada(self):
        if self.status == 'informada':
            self.status = 'cancelada'
            self.save()
            return "Entrada cancelada"

        return "Não foi possivel cancelar esta entrada"

    def expirar_entrada(self):
        if self.status == 'informada':
            self.status = 'expirada'
            self.save()
            return "Entrada expirada"

        return "Não foi possivel expirar esta entrada"

    def __str__(self):
        return self.descricao


class Aviso(Base):

    PRIORIDADE_AVISO = (
        ('baixa', 'Baixa'),
        ('razoavel', 'Razoavel'),
        ('urgente', 'Urgente'),
    )

    informante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='avisos', blank=False, null=False)
    descricao = models.CharField('Descricao', max_length=256, blank=True, null=True)
    prioridade = models.CharField('Prioridade', choices=PRIORIDADE_AVISO, default='razoavel', max_length=256, blank=False, null=False)

    class Meta:
        verbose_name = 'Aviso'
        verbose_name_plural = 'Avisos'

    def __str__(self):
        return self.descricao


class Visitante(Base):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )

    nome = models.CharField('Nome', max_length=256, blank=False, null=False)
    sexo = models.CharField('Sexo', max_length=16, choices=SEXO_CHOICES, blank=False, null=False)
    telefone = models.CharField('Telefone', max_length=16, blank=False, null=False)
    data_nascimento = models.DateField('Data de nascimento', blank=False, null=False)

    unidade_habitacional = models.ForeignKey(UnidadeHabitacional, on_delete=models.CASCADE, related_name='visitantes', blank=False, null=False)

    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def __str__(self):
        return self.nome