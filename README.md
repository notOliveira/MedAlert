# Medalert - Django

### Leia tudo, mas principalmente as [instruções iniciais](#preparacao), para que o projeto funcione.

<br>

<h2 id="preparacao"> Para preparar a inicialização da aplicação</h2>

<br>

### Criando ambiente virtual

```
python -m venv <name venv>
```

<br>

## Iniciando ambiente virtual

#### Linux

```
source venv/bin/activate
```

#### Windows

```
.\venv\Scripts\activate
```

<br>

## Desativando ambiente virtual
- Desative apenas se não irá mais utilizar o projeto

<br>

```
deactivate
```

---

<br>

### Instalando dependências
- Instale na venv preferencialmente

```
(venv) pip install -r requirements.txt
```
<br>

---

<br>


## Aplicando as migrações

```
python manage.py makemigrations // Provavelmente não será necessário, porque deixarei um arquivo com a migração inicial
python manage.py migrate
```

<br>

## Criando dados para exemplo

```
python manage.py create_data
```

- Irá criar um superusuário e alguns dados de médicos, pacientes e receitas.

<br>

## Coletando arquivos estáticos

```
python manage.py collectstatic
```

<br>

## Iniciar o projeto (endereço e porta opcionais, porta padrão 8000)


```
python manage.py runserver <endereço IP>:<port>
```

<br>

OBS: Recomendo rodar com o seguinte comando:

```
python.exe .\manage.py runserver 0.0.0.0:8000
```

<br>

- Crie um arquivo [.env](/.env) com as seguintes informações:

```
# General configs

DEBUG=True
ENVIRONMENT=sqlite / local / production # Escolha se usará o SQLITE, mysql local ou banco de produção
SECRET_KEY='?'
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=http://localhost:<porta frontend>
CORS_ALLOWED_ORIGINS=*
FRONTEND_URL=http://localhost:5173

# Database - Local

DB_DATABASE=?
DB_USER=?
DB_PASSWORD=?
DB_HOST=?
DB_PORT=?

# Database - Production

PROD_DATABASE=?
PROD_USER=?
PROD_PASSWORD=?
PROD_HOST=?
PROD_PORT=?


# Email

EMAIL_HOST_USER=?
EMAIL_HOST_PASSWORD=?

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=?
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=?
```

## Para rodar os testes

```
python manage.py test --verbosity=2
```

- OBS: o parâmetro opctional "--verbosity=n" também pode ser usado, com "n" sendo um número de 0 a 3 que identifica os níveis de logs que serão exibidos nos testes, com 0 sendo uma quantidade menor e 3 sendo a quantidade maior. O verbosity 2 é o mais recomendado.

## Configuração de aplicativo social


![alt text](/static/readme/image.png)
```json
{
    "scope": [
        "profile",
        "email"
    ]
}
```