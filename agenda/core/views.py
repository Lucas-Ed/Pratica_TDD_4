from django.shortcuts import render, redirect, get_object_or_404
from core.forms import LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Agenda
from .forms import AgendaForm
from django.contrib import messages


def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)

# ---------------- CRUD DA AGENDA ----------------

@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def listar_contatos(request):
    contatos = Agenda.objects.all()
    return render(request, 'listar.html', {'contatos': contatos})


@login_required
def cadastrar_contato(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato cadastrado com sucesso!')
            return redirect('listar_contatos')
    else:
        form = AgendaForm()
    return render(request, 'cadastrar.html', {'form': form})


@login_required
def editar_contato(request, id):
    contato = get_object_or_404(Agenda, id=id)
    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=contato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato atualizado com sucesso!')
            return redirect('listar_contatos')
    else:
        form = AgendaForm(instance=contato)
    return render(request, 'editar.html', {'form': form})


@login_required
def excluir_contato(request, id):
    contato = get_object_or_404(Agenda, id=id)
    if request.method == 'POST':
        contato.delete()
        messages.success(request, 'Contato removido com sucesso!')
        return redirect('listar_contatos')
    return render(request, 'excluir.html', {'contato': contato})