from django import forms
from .models import Foto
from .models import Comentario

class FotoForm(forms.ModelForm):
  class Meta:
    model = Foto
    fields = ['imagem', 'descricao']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
