# Registro epidemiológico

O projeto está disponível no link [https://registro-epidemiologico.herokuapp.com](https://registro-epidemiologico.herokuapp.com). 

## Instalação
Para rodar no modo local, inicialmente é necessário criar um arquivo 
``local_settings.py`` no diretório `registro-epidemiologico`
seguindo o seguinte formato
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': <nome_banco>,
        'USER': <usuario>,
        'PASSWORD': <senha>,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

SECRET_KEY = <chave>

DEBUG = True

ALLOWED_HOSTS = ['*']
```

Depois basta rodar o comando abaixo para instalar as dependências
do projeto
``` 
pip instal -r requirements.txt
```

É então preciso gerar as migrações com a instrução

```
python manage.py makemigrations
```

E executar as migrações

```
python manage.py migrate
```

Para ter acesso ao sistema, antes deve-se utilizar
o  

```
python manage.py createsuperuser
```

Por fim, basta executar o comando para iniciar a aplicação e acessar
```
python manage.py runserver
```