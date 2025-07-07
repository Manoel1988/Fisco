#!/bin/bash

# Build mínimo para Netlify - foca apenas no essencial
echo "🚀 Build mínimo para Netlify"

# Instalar apenas o Django e WhiteNoise
echo "📦 Instalando dependências mínimas..."
pip install Django==5.1.4 whitenoise==6.6.0

# Criar diretório de estáticos
echo "📁 Criando diretório staticfiles..."
mkdir -p staticfiles

# Coletar arquivos estáticos
echo "🎨 Coletando arquivos estáticos..."
DJANGO_SETTINGS_MODULE=netlify_settings python manage.py collectstatic --noinput --clear

echo "✅ Build mínimo concluído!" 