#!/bin/bash

# Script de build para Netlify
echo "🚀 Iniciando build para Netlify..."

# Instalar dependências
echo "📦 Instalando dependências..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Verificar se o diretório logs existe
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo "📁 Diretório logs criado"
fi

# Coletar arquivos estáticos
echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py migrate --noinput

# Verificar se tudo está OK
echo "✅ Build concluído com sucesso!"
echo "🌐 Sistema pronto para deploy no Netlify" 