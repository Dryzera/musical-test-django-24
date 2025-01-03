from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Localidade(models.Model):
    localidade = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return self.localidade

class UserPerfil(models.Model):
    CATEGORIAS_CHOICES = [
        ('Cordas', 'Cordas'),
        ('Madeiras', 'Madeiras'),
        ('Metais', 'Metais'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    localidade = models.ForeignKey(Localidade, on_delete=models.SET_NULL, null=True)
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=False)
    categoria = models.CharField(choices=CATEGORIAS_CHOICES, max_length=10, blank=False)

    class Meta:
        verbose_name = 'Perfil de úsuario'

    def __str__(self):
        return f'Perfil de {self.user}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.user and self.grupo:
            self.user.groups.add(self.grupo)

            if self.grupo.name == 'instrutores':
                self.user.is_staff = True
                self.user.save()

class Perguntas(models.Model):
    FASES_MSA_CHOICES = [
        ('1', 'Fase 1'),
        ('2', 'Fase 2'),
        ('3', 'Fase 3'),
        ('4', 'Fase 4'),
        ('5', 'Fase 5'),
        ('6', 'Fase 6'),
        ('7', 'Fase 7'),
        ('8', 'Fase 8'),
        ('9', 'Fase 9'),
        ('10', 'Fase 10'),
        ('11', 'Fase 11'),
        ('12', 'Fase 12'),
        ('13', 'Fase 13'),
        ('14', 'Fase 14'),
        ('15', 'Fase 15'),
        ('16', 'Fase 16'),
        ('N/D', 'Sem Fase'),
    ]
    NIVEL_DIFICULDADE_CHOICE = [
        ('Muito Facil', 'Muito Facil'),
        ('Facil', 'Facil'),
        ('Intermediário', 'Intermediário'),
        ('Difícil', 'Difícil'),
        ('Muito Difícil', 'Muito Difícil'),
    ]


    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    pergunta = models.CharField(max_length=200)
    fase = models.CharField(choices=FASES_MSA_CHOICES, max_length=10, blank=False)
    dificuldade = models.CharField(choices=NIVEL_DIFICULDADE_CHOICE, max_length=13, blank=False)


    class Meta:
        verbose_name_plural = 'Perguntas'

    def __str__(self):
        return self.pergunta

class Respostas(models.Model):
    pergunta = models.ForeignKey(Perguntas, on_delete=models.CASCADE, related_name="respostas")
    resposta = models.CharField(max_length=200, blank=False)
    resposta_correta = models.BooleanField(default=False)

class Jogo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    finished_at = models.DateTimeField(verbose_name='Terminado em', null=True, blank=True)
    qtd_erros = models.PositiveIntegerField(default=0)
    qtd_acertos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Jogo de {self.user}'

class PerguntasJogo(models.Model):
    game = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name="perguntas_jogo")
    question = models.ForeignKey(Perguntas, on_delete=models.SET_NULL, null=True, related_name="jogos")

    def __str__(self):
        return f'Perguntas do jogo {self.game}'
