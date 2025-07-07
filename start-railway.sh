#!/bin/bash

# Script de inicialização para Railway
echo "🚀 Iniciando aplicação no Railway..."

# Verificar variáveis de ambiente
echo "🔍 Verificando configurações..."
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DEBUG: $DEBUG"
echo "PORT: $PORT"

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p logs staticfiles media

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Verificar se o banco de dados está funcionando
echo "🔍 Verificando banco de dados..."
python manage.py check --database default

# Criar superusuário se não existir
echo "👤 Verificando superusuário..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado: admin/admin123')
else:
    print('Superusuário já existe')
"

# Iniciar servidor
echo "🌐 Iniciando servidor Gunicorn..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --log-level info \
    --access-logfile - \
    --error-logfile - 