from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from base.forms import PacienteForm
from base.models import User


def autocadastro(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf'].replace('-', '').replace('.', '')
            usuario = User.objects.get_or_create(username=cpf)[0]
            print(usuario)
            # todo: verificar se usuario ja esta criado
            usuario.username = cpf
            usuario.cpf = form.cleaned_data['cpf']
            usuario.nome = form.cleaned_data['nome']
            usuario.nome_mae = form.cleaned_data['nome_mae']
            usuario.data_nascimento = form.cleaned_data['data_nascimento']
            usuario.email = form.cleaned_data['email']
            usuario.sexo = form.cleaned_data['sexo']
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('autocadastro')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PacienteForm()

    return render(request, 'form.html', {'form': form})
