#!/bin/bash

# Script de inicialização simplificado para Railway
echo "🚀 Iniciando Sistema Fisco no Railway..."

# Definir configurações
export DJANGO_SETTINGS_MODULE=railway_settings_minimal
export PYTHONUNBUFFERED=1
export DEBUG=False

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p staticfiles media logs

# Coletar arquivos estáticos (sem --clear para evitar erros)
echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || echo "⚠️ Erro ao coletar estáticos, continuando..."

# Executar migrações com tratamento de erro
echo "🗄️ Executando migrações..."
python manage.py migrate --noinput || echo "⚠️ Erro nas migrações, continuando..."

# Verificar se consegue acessar o Django
echo "🔍 Testando Django..."
python manage.py check || echo "⚠️ Problemas detectados, mas continuando..."

# Iniciar servidor Gunicorn
echo "🌐 Iniciando servidor..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 60 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile - \
    --error-logfile - 