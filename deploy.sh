#!/bin/bash

# 🚀 Script de Deploy do Sistema Fisco
# Automatiza o processo de deploy para GitHub e plataformas de hospedagem

set -e

echo "🚀 Iniciando deploy do Sistema Fisco..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se está no diretório correto
if [ ! -f "manage.py" ]; then
    print_error "Este script deve ser executado no diretório raiz do projeto Django!"
    exit 1
fi

# Verificar se o Git está configurado
if ! git config user.name &> /dev/null; then
    print_error "Git não está configurado. Configure com:"
    echo "git config --global user.name 'Seu Nome'"
    echo "git config --global user.email 'seu.email@exemplo.com'"
    exit 1
fi

# Verificar se há mudanças para commit
if git diff --quiet && git diff --cached --quiet; then
    print_warning "Nenhuma mudança detectada para commit."
else
    print_status "Adicionando arquivos ao Git..."
    git add .
    
    # Solicitar mensagem de commit
    read -p "Digite a mensagem do commit (ou pressione Enter para usar padrão): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="feat: atualização do sistema"
    fi
    
    print_status "Fazendo commit..."
    git commit -m "$commit_msg"
    print_success "Commit realizado com sucesso!"
fi

# Verificar se o remote origin está configurado
if ! git remote get-url origin &> /dev/null; then
    print_warning "Remote 'origin' não configurado."
    read -p "Digite a URL do repositório GitHub (ex: https://github.com/usuario/repo.git): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        print_success "Remote origin configurado: $repo_url"
    else
        print_error "URL do repositório é obrigatória!"
        exit 1
    fi
fi

# Push para GitHub
print_status "Enviando código para GitHub..."
git push -u origin main
print_success "Código enviado para GitHub com sucesso!"

# Verificar requirements.txt
print_status "Verificando requirements.txt..."
if [ -f "requirements.txt" ]; then
    print_success "requirements.txt encontrado"
else
    print_warning "requirements.txt não encontrado. Gerando..."
    pip freeze > requirements.txt
    git add requirements.txt
    git commit -m "feat: adicionar requirements.txt"
    git push origin main
fi

# Verificar arquivos de configuração
print_status "Verificando arquivos de configuração..."

configs_found=()
if [ -f "Procfile" ]; then
    configs_found+=("Procfile (Heroku)")
fi
if [ -f "railway.toml" ]; then
    configs_found+=("railway.toml (Railway)")
fi
if [ -f "render.yaml" ]; then
    configs_found+=("render.yaml (Render)")
fi

if [ ${#configs_found[@]} -gt 0 ]; then
    print_success "Arquivos de configuração encontrados:"
    for config in "${configs_found[@]}"; do
        echo "  ✅ $config"
    done
else
    print_warning "Nenhum arquivo de configuração de deploy encontrado!"
fi

# Mostrar próximos passos
print_success "🎉 Deploy preparado com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. 🌐 Escolha uma plataforma de deploy:"
echo "   • Railway (Recomendado): https://railway.app"
echo "   • Render: https://render.com"
echo "   • Heroku: https://heroku.com"
echo ""
echo "2. 🔗 Conecte sua conta GitHub à plataforma"
echo ""
echo "3. 📦 Selecione o repositório: $(git remote get-url origin)"
echo ""
echo "4. ⚙️ Configure as variáveis de ambiente:"
echo "   • DEBUG=false"
echo "   • SECRET_KEY=sua-chave-secreta"
echo "   • ALLOWED_HOSTS=.railway.app (ou domínio da plataforma)"
echo "   • DEEPSEEK_API_KEY=sua-chave-deepseek (opcional)"
echo ""
echo "5. 🚀 Deploy automático será executado!"
echo ""
echo "📚 Documentação completa: README_DEPLOY.md"
echo ""
print_success "Sistema pronto para deploy! 🎯" 