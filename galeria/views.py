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
from django.shortcuts import render

def is_superuser(user):
    return user.is_superuser

def is_casal(user):
    # Aqui você pode definir a regra para "casal" se quiser
    return user.is_superuser  # por exemplo, superuser é casal


@login_required
def home(request):
    fotos = Foto.objects.filter(aprovada=True).order_by('-data_criacao')
    return render(request, 'home.html', {'fotos': fotos})


@login_required
def upload_foto(request):
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.autor = request.user
            foto.save()
            messages.success(request, "Foto enviada com sucesso!")
            return redirect('home')
    else:
        form = FotoForm()
    return render(request, 'upload_foto.html', {'form': form})


@login_required
def galeria(request):
    fotos = Foto.objects.filter(aprovada=True).order_by('-data_criacao')
    return render(request, 'galeria.html', {'fotos': fotos})


@user_passes_test(is_casal)
def aprovacao_fotos(request):
    fotos_pendentes = Foto.objects.filter(aprovada=False).order_by('data_criacao')

    if request.method == 'POST':
        foto_id = request.POST.get('foto_id')
        acao = request.POST.get('acao')
        try:
            foto = Foto.objects.get(id=foto_id)
            if acao == 'aprovar':
                foto.aprovada = True
                foto.save()
                messages.success(request, f"Foto {foto_id} aprovada.")
            elif acao == 'rejeitar':
                foto.delete()
                messages.success(request, f"Foto {foto_id} rejeitada e deletada.")
        except Foto.DoesNotExist:
            messages.error(request, "Foto não encontrada.")
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
    curtida_existente = foto.curtidas.filter(usuario=usuario).first()

    if not curtida_existente:
        foto.curtidas.create(usuario=usuario)

    return redirect('galeria')


def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registrar.html', {'form': form})


@user_passes_test(is_superuser)
def deletar_foto(request, foto_id):
    foto = get_object_or_404(Foto, id=foto_id)
    if request.method == 'POST':
        foto.delete()
        messages.success(request, "Foto deletada com sucesso.")
    return redirect('galeria')
