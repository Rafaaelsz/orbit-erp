#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Correção: Usando colchetes simples [ ] para compatibilidade com 'sh'
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Criando superusuário..."
    python manage.py createsuperuser --noinput || echo "Superusuário já existe."
fi