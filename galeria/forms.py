from django import forms
from .models import Foto
from .models import Comentario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FotoForm(forms.ModelForm):
  class Meta:
    model = Foto
    fields = ['imagem', 'descricao']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
  
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')