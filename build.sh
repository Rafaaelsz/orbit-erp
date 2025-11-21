#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Instala as dependências
pip install -r requirements.txt

# 2. Coleta os arquivos estáticos (CSS, JS, Imagens do Admin)
python manage.py collectstatic --no-input

# 3. Cria as tabelas no banco de dados
python manage.py migrate

# 4. Automação: Cria o superusuário se as variáveis existirem no Render
# Isso evita que você precise usar o Shell pago
if [[ -n "$DJANGO_SUPERUSER_USERNAME" ]] && [[ -n "$DJANGO_SUPERUSER_EMAIL" ]]; then
    echo "Criando superusuário..."
    python manage.py createsuperuser --noinput || echo "Superusuário já existe."
fi