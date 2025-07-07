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

# Criar superusuário se não existir
echo "👤 Criando superusuário..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fisco.com', 'admin123')
    print('✅ Superusuário criado: admin/admin123')
else:
    print('ℹ️ Superusuário já existe')
" || echo "⚠️ Erro ao criar superusuário, continuando..."

# Importar dados se os arquivos existirem
echo "📥 Verificando dados para importação..."
if [ -f "usuarios.json" ]; then
    echo "📥 Importando usuários..."
    python manage.py loaddata usuarios.json || echo "⚠️ Erro ao importar usuários, continuando..."
fi

if [ -f "dados_auditoria.json" ]; then
    echo "📥 Importando dados de auditoria (pode demorar)..."
    python manage.py loaddata dados_auditoria.json || echo "⚠️ Erro ao importar dados de auditoria, continuando..."
fi

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