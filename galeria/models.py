from django.db import models
from django.contrib.auth.models import User  # Usuário padrão do Django

# Modelo para armazenar as fotos enviadas pelos amigos
class Foto(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='fotos/')
    descricao = models.TextField(blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    aprovada = models.BooleanField(default=False)

    def __str__(self):
        return f"Foto {self.id} por {self.autor.username}"

# Modelo para armazenar os comentários feitos nas fotos
class Comentario(models.Model):
    foto = models.ForeignKey(Foto, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.username} na foto {self.foto.id}"

# Modelo para armazenar as curtidas das fotos
class Curtida(models.Model):
    foto = models.ForeignKey(Foto, related_name='curtidas', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('foto', 'usuario')

    def __str__(self):
        return f"Curtida de {self.usuario.username} na foto {self.foto.id}"
