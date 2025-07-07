#!/bin/bash

# Build script otimizado para Netlify
set -e  # Para em caso de erro

echo "🚀 Iniciando build otimizado para Netlify..."

# Verificar versão do Python
echo "🐍 Versão do Python:"
python --version

# Atualizar pip
echo "📦 Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências essenciais
echo "📋 Instalando dependências essenciais..."
if [ -f "requirements-netlify.txt" ]; then
    pip install -r requirements-netlify.txt
else
    echo "⚠️  Arquivo requirements-netlify.txt não encontrado, usando requirements.txt"
    pip install -r requirements.txt
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media

# Verificar se Django está instalado
echo "🔍 Verificando Django..."
python -c "import django; print(f'Django {django.get_version()} instalado com sucesso')"

# Coletar arquivos estáticos (sem fail em caso de erro)
echo "🎨 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Erro ao coletar arquivos estáticos, continuando..."

# Verificar se o banco existe
if [ -f "db.sqlite3" ]; then
    echo "🗄️  Banco de dados SQLite encontrado"
else
    echo "⚠️  Banco de dados não encontrado, criando novo..."
    python manage.py migrate --noinput || echo "⚠️  Erro nas migrações, continuando..."
fi

# Verificar estrutura final
echo "📊 Verificando estrutura final..."
ls -la staticfiles/ || echo "⚠️  Diretório staticfiles não encontrado"

echo "✅ Build concluído!"
echo "🌐 Sistema pronto para Netlify" 