from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from base import utils
from base.forms import PacienteForm
from base.models import User, Paciente


def autocadastro(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
            usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
            utils.salva_usuario(usuario, form, cpf)
            paciente = Paciente()
            paciente.usuario = usuario
            paciente.descricao_caso = form.cleaned_data['descricao_caso']
            paciente.save()
            return redirect('autocadastro')

    else:
        form = PacienteForm()

    return render(request, 'form.html', {'form': form})
