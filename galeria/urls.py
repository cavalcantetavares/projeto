from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), 
    path('upload/', views.upload_foto, name='upload_foto'),
    path('galeria/', views.galeria, name='galeria'),
    path('aprovacao/', views.aprovacao_fotos, name='aprovacao_fotos'),
    path('foto/<int:foto_id>/comentar/', views.comentar_foto, name='comentar_foto'),
    path('foto/<int:foto_id>/curtir/', views.curtir_foto, name='curtir_foto'),
    path('registrar/', views.registrar, name='registrar'),
    path('foto/<int:foto_id>/deletar/', views.deletar_foto, name='deletar_foto'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]