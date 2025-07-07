#!/bin/bash

# Build universal para Netlify - funciona com qualquer Python disponível
set -e

echo "🚀 Build universal para Netlify"
echo "🐍 Detectando Python disponível..."

# Detectar versão do Python disponível
PYTHON_CMD="python3"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python não encontrado!"
    exit 1
fi

echo "✅ Usando: $PYTHON_CMD"
$PYTHON_CMD --version

# Atualizar pip
echo "📦 Atualizando pip..."
$PYTHON_CMD -m pip install --upgrade pip

# Instalar dependências mínimas
echo "🔧 Instalando Django e WhiteNoise..."
$PYTHON_CMD -m pip install "Django>=4.0,<6.0" "whitenoise>=6.0"

# Verificar instalação
echo "🔍 Verificando instalação..."
$PYTHON_CMD -c "import django; print(f'Django {django.get_version()} instalado')"
$PYTHON_CMD -c "import whitenoise; print('WhiteNoise instalado')"

# Criar diretórios
echo "📁 Criando diretórios..."
mkdir -p staticfiles
mkdir -p logs

# Coletar arquivos estáticos
echo "🎨 Coletando arquivos estáticos..."
export DJANGO_SETTINGS_MODULE=netlify_settings
$PYTHON_CMD manage.py collectstatic --noinput --clear

# Verificar resultado
echo "📊 Verificando resultado..."
if [ -d "staticfiles" ] && [ "$(ls -A staticfiles)" ]; then
    echo "✅ Arquivos estáticos coletados com sucesso!"
    ls -la staticfiles/ | head -10
else
    echo "⚠️ Diretório staticfiles vazio ou não encontrado"
fi

echo "🎉 Build universal concluído com sucesso!" 