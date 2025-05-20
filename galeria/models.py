from django.db import models
from django.contrib.auth.models import User  # Usuário padrão do Django
from django.utils import timezone


class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    administradores = models.ManyToManyField(User, related_name='grupos_administrando')
    membros = models.ManyToManyField(User, related_name='grupos_participando')

    def __str__(self):
        return self.nome

class Foto(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='fotos/')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    aprovada = models.BooleanField(default=False)

    def __str__(self):
        return f'Foto {self.id} por {self.autor.username}'

class Comentario(models.Model):
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username}'

class Curtida(models.Model):
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name='curtidas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'Curtida de {self.usuario.username} na foto {self.foto.id}'