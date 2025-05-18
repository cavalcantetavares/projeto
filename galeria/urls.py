from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('upload/', views.upload_foto, name='upload_foto'), # Sua view home, vamos criar a seguir
    path('galeria/', views.galeria, name='galeria'),
    path('aprovacao/', views.aprovacao_fotos, name='aprovacao_fotos'),
    path('foto/<int:foto_id>/comentar/', views.comentar_foto, name='comentar_foto'),
    path('foto/<int:foto_id>/curtir/', views.curtir_foto, name='curtir_foto'),
]
