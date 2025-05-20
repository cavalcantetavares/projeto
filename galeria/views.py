from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FotoForm
from .models import Foto
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import ComentarioForm
from django.shortcuts import get_object_or_404
from .forms import RegistroForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect


@login_required
def home(request):
   return render(request, 'home.html')

@login_required
def upload_foto(request):
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.autor = request.user
            foto.save()
            return redirect('home')
    else:
        form = FotoForm()
    return render(request, 'upload_foto.html', {'form': form})    

@login_required
def galeria(request):
    fotos = Foto.objects.filter(aprovada=True).order_by('-data_envio')
    return render(request, 'galeria.html', {'fotos':fotos})

def is_casal(user):
    return user.is_superuser
       


def is_casal(user):
    return user.is_superuser

@user_passes_test(is_casal)
def aprovacao_fotos(request):
    print("Acessando a aprovação de fotos...")
    fotos_pendentes = Foto.objects.filter(aprovada=False).order_by('data_envio')
    print(f"Fotos pendentes: {fotos_pendentes}")
    
    if request.method == 'POST':
        print("Formulário enviado...")
        foto_id = request.POST.get('foto_id')
        acao = request.POST.get('acao')
        print(f"Foto ID: {foto_id}, Ação: {acao}")
        
        try:
            foto = Foto.objects.get(id=foto_id)
            if acao == 'aprovar':
                foto.aprovada = True
                foto.save()
                print(f"Foto {foto.id} aprovada.")
            elif acao == 'rejeitar':
                foto.delete()
                print(f"Foto {foto.id} rejeitada e deletada.")
        except Foto.DoesNotExist:
            print(f"Foto com ID {foto_id} não encontrada.")
        
        return redirect('aprovacao_fotos')

    return render(request, 'aprovacao_fotos.html', {'fotos': fotos_pendentes})
@login_required
def comentar_foto(request, foto_id):
    foto = get_object_or_404(Foto, id=foto_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.foto = foto
            comentario.save()
            messages.success(request, "Comentário adicionado com sucesso.")
            return redirect('galeria')

    else:
        form = ComentarioForm()

    return render(request, 'comentar_foto.html', {'form': form, 'foto': foto})
@login_required
def curtir_foto(request, foto_id):
    foto = get_object_or_404(Foto, id=foto_id)
    usuario = request.user

    # Verifica se o usuário já curtiu a foto
    curtida_existente = foto.curtidas.filter(usuario=usuario).first()

    if not curtida_existente:
        # Cria a curtida
        foto.curtidas.create(usuario=usuario)
    
    return redirect('galeria')


def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login .")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registrar.html', {'form': form})          

@staff_member_required
def deletar_foto(request, foto_id):
    foto = get_object_or_404(Foto, id=foto_id)
    if request.method == 'POST':
        foto.delete()
        messages.success(request, "Foto deletada com sucesso.")
        return redirect('aprovacao_fotos')

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def deletar_foto(request, foto_id):    
    foto = get_object_or_404(Foto, id=foto_id)
    if request.method == 'POST':
        foto.delete()        
        return redirect('galeria')   
    return redirect('galeria')
                        