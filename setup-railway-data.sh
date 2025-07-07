#!/bin/bash

# Script para configurar dados no Railway após deploy
echo "🗄️ Configurando dados no Railway..."

# Definir configurações
export DJANGO_SETTINGS_MODULE=railway_settings_minimal
export PYTHONUNBUFFERED=1

# Executar migrações
echo "📋 Executando migrações..."
python manage.py migrate --noinput

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
"

# Importar dados se os arquivos existirem
if [ -f "usuarios.json" ]; then
    echo "📥 Importando usuários..."
    python manage.py loaddata usuarios.json
    echo "✅ Usuários importados!"
fi

if [ -f "dados_auditoria.json" ]; then
    echo "📥 Importando dados de auditoria..."
    python manage.py loaddata dados_auditoria.json
    echo "✅ Dados de auditoria importados!"
fi

# Coletar arquivos estáticos
echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "🎉 Configuração concluída!" 