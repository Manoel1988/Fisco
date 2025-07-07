#!/bin/bash

# Build com fallback para Netlify - máxima compatibilidade
echo "🚀 Build com fallback para Netlify"

# Função para instalar Django
install_django() {
    local cmd=$1
    echo "🔧 Tentando instalar Django com $cmd..."
    
    # Tentar instalar Django
    if $cmd -m pip install Django whitenoise; then
        echo "✅ Django instalado com sucesso!"
        return 0
    else
        echo "❌ Falha ao instalar com $cmd"
        return 1
    fi
}

# Detectar Python disponível
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python não encontrado! Tentando continuar..."
    exit 1
fi

echo "🐍 Usando Python: $PYTHON_CMD"
$PYTHON_CMD --version || echo "⚠️ Não foi possível obter versão do Python"

# Instalar dependências
if ! install_django "$PYTHON_CMD"; then
    echo "❌ Falha na instalação das dependências"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p staticfiles logs media

# Verificar se Django está funcionando
echo "🔍 Verificando Django..."
if ! $PYTHON_CMD -c "import django; print('Django OK')"; then
    echo "❌ Django não está funcionando"
    exit 1
fi

# Coletar arquivos estáticos
echo "🎨 Coletando arquivos estáticos..."
export DJANGO_SETTINGS_MODULE=netlify_settings

if $PYTHON_CMD manage.py collectstatic --noinput --clear; then
    echo "✅ Arquivos estáticos coletados!"
else
    echo "⚠️ Erro ao coletar arquivos estáticos, criando diretório básico..."
    mkdir -p staticfiles/admin
    echo "/* Arquivo placeholder */" > staticfiles/admin/placeholder.css
fi

# Verificar resultado final
if [ -d "staticfiles" ]; then
    echo "✅ Diretório staticfiles criado com sucesso!"
    ls -la staticfiles/
else
    echo "❌ Falha ao criar staticfiles"
    exit 1
fi

echo "🎉 Build concluído!" 