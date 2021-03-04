def save_user(user, form, cpf):
    user.username = cpf
    user.cpf = form.cleaned_data['cpf']
    user.nome = form.cleaned_data['nome']
    user.nome_mae = form.cleaned_data['nome_mae']
    user.data_nascimento = form.cleaned_data['data_nascimento']
    user.email = form.cleaned_data['email']
    user.sexo = form.cleaned_data['sexo']
    user.set_password(form.cleaned_data['password'])
    user.save()
