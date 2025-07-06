#!/bin/bash

# Script para automatizar deploy no GitHub
# Uso: ./deploy.sh "mensagem do commit"

# Verificar se foi fornecida uma mensagem de commit
if [ $# -eq 0 ]; then
    echo "Uso: ./deploy.sh \"mensagem do commit\""
    echo "Exemplo: ./deploy.sh \"Adicionada nova funcionalidade\""
    exit 1
fi

# Adicionar todos os arquivos modificados
echo "📝 Adicionando arquivos modificados..."
git add .

# Fazer commit com a mensagem fornecida
echo "💾 Fazendo commit..."
git commit -m "$1"

# Verificar se existe remote origin
if git remote get-url origin > /dev/null 2>&1; then
    echo "🚀 Enviando para GitHub..."
    git push origin main
    echo "✅ Deploy concluído com sucesso!"
else
    echo "❌ Remote 'origin' não configurado."
    echo "Configure primeiro o remote com:"
    echo "git remote add origin https://github.com/SEU_USUARIO/fisco.git"
    echo "git push -u origin main"
fi 