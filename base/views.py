from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from base import utils
from base.forms import PacienteForm
from base.models import User


def autocadastro(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
            usuario = User.objects.get_or_create(username=cpf, is_staff=True)[0]
            # todo: verificar se usuario ja esta criado
            utils.save_user(usuario, form, cpf)
            return redirect('autocadastro')

    else:
        form = PacienteForm()

    return render(request, 'form.html', {'form': form})
