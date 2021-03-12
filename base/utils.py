import datetime


def salva_usuario(user, form, cpf):
    user.username = cpf
    user.cpf = form.cleaned_data['cpf']
    user.nome = form.cleaned_data['nome']
    user.nome_mae = form.cleaned_data['nome_mae']
    user.data_nascimento = form.cleaned_data['data_nascimento']
    user.email = form.cleaned_data['email']
    user.sexo = form.cleaned_data['sexo']
    user.municipio = form.cleaned_data['municipio']
    user.eh_gestor = form.cleaned_data['eh_gestor'] if 'eh_gestor' in form.cleaned_data else False
    user.set_password(form.cleaned_data['password'])
    user.save()


def calcula_faixa_etaria(data_nascimento):
    classes = [(0, 18), (19, 25), (26, 35), (36, 50), (51, 60), (61, 70),
               (71, 80), (81, 100)]

    idade = (datetime.date.today() - data_nascimento).days / 365
    for i, f in classes:
        if i <= idade <= f:
            return f"{i:02}-{f:02}"

    return ">100"
