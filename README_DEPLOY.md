# 🚀 Deploy do Sistema Fisco - Auditoria Fiscal

## Visão Geral

Este guia mostra como fazer deploy do sistema Fisco (Sistema de Auditoria Fiscal com IA) usando GitHub e diferentes plataformas de hospedagem.

## 📋 Pré-requisitos

- ✅ Conta no GitHub
- ✅ Código do projeto pronto
- ✅ Conta em uma plataforma de deploy (Railway, Render, ou Heroku)
- ✅ Chave da API DeepSeek (opcional, para IA)

## 🔧 Configuração Inicial

### 1. Preparar o Repositório Git

```bash
# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "feat: Sistema completo de auditoria fiscal com upload PDF TIPI"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/fisco-auditoria.git
git branch -M main
git push -u origin main
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` e configure as variáveis:

```bash
cp .env.example .env
```

**Variáveis obrigatórias:**
- `SECRET_KEY`: Chave secreta do Django
- `DEBUG`: False para produção
- `ALLOWED_HOSTS`: Domínios permitidos
- `DATABASE_URL`: URL do banco de dados
- `DEEPSEEK_API_KEY`: Chave da API DeepSeek (opcional)

## 🌐 Opções de Deploy

### Opção 1: Railway (Recomendado)

**Vantagens:**
- ✅ Deploy automático via GitHub
- ✅ Banco PostgreSQL incluído
- ✅ SSL automático
- ✅ $5/mês de crédito gratuito

**Passos:**
1. Acesse [railway.app](https://railway.app)
2. Conecte sua conta GitHub
3. Selecione o repositório `fisco-auditoria`
4. Configure as variáveis de ambiente
5. Deploy automático!

**Variáveis no Railway:**
```
DEBUG=false
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=.railway.app
DEEPSEEK_API_KEY=sua-chave-deepseek
```

### Opção 2: Render

**Vantagens:**
- ✅ Plano gratuito disponível
- ✅ Deploy automático via GitHub
- ✅ SSL automático
- ✅ Banco PostgreSQL gratuito

**Passos:**
1. Acesse [render.com](https://render.com)
2. Conecte sua conta GitHub
3. Selecione o repositório
4. Use o arquivo `render.yaml` para configuração automática
5. Configure as variáveis de ambiente

### Opção 3: Heroku

**Vantagens:**
- ✅ Plataforma tradicional e estável
- ✅ Muitos add-ons disponíveis
- ✅ Documentação extensa

**Passos:**
1. Instale o Heroku CLI
2. Faça login: `heroku login`
3. Crie o app: `heroku create fisco-auditoria`
4. Configure variáveis: `heroku config:set SECRET_KEY=sua-chave`
5. Deploy: `git push heroku main`

## 🗄️ Configuração do Banco de Dados

### PostgreSQL (Recomendado para produção)

```bash
# Instalar driver PostgreSQL
pip install psycopg2-binary

# Adicionar ao requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt
```

**URL de conexão:**
```
DATABASE_URL=postgresql://usuario:senha@host:5432/banco
```

### SQLite (Desenvolvimento)

```
DATABASE_URL=sqlite:///db.sqlite3
```

## 🔐 Configuração de Segurança

### Variáveis de Ambiente de Produção

```bash
# Gerar nova SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Configurar no deploy
DEBUG=false
SECRET_KEY=nova-chave-super-secreta
ALLOWED_HOSTS=seu-dominio.com,.railway.app
```

### SSL e HTTPS

O sistema está configurado para HTTPS automático em produção:
- ✅ SSL redirect habilitado
- ✅ Cookies seguros
- ✅ Headers de segurança
- ✅ HSTS configurado

## 📊 Monitoramento

### Logs da Aplicação

```bash
# Railway
railway logs

# Heroku
heroku logs --tail

# Render
# Logs disponíveis no dashboard
```

### Health Check

O sistema possui health check em `/admin/` para monitoramento automático.

## 🔄 Deploy Automático

### GitHub Actions (Opcional)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to Railway
      uses: railway-app/railway-action@v1
      with:
        railway_token: ${{ secrets.RAILWAY_TOKEN }}
        railway_service: fisco-auditoria
```

## 📝 Checklist de Deploy

### Antes do Deploy
- [ ] Código commitado no GitHub
- [ ] Variáveis de ambiente configuradas
- [ ] Requirements.txt atualizado
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configurado
- [ ] Arquivos estáticos configurados

### Após o Deploy
- [ ] Aplicação carregando
- [ ] Admin acessível
- [ ] Upload de PDF funcionando
- [ ] Banco de dados funcionando
- [ ] Logs sem erros críticos
- [ ] SSL funcionando

## 🛠️ Solução de Problemas

### Erro: "Application Error"
```bash
# Verificar logs
railway logs
# ou
heroku logs --tail

# Verificar variáveis de ambiente
railway variables
# ou
heroku config
```

### Erro: "Static files not found"
```bash
# Executar collectstatic
python manage.py collectstatic --noinput

# Verificar STATIC_ROOT no settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Erro: "Database connection failed"
```bash
# Verificar DATABASE_URL
echo $DATABASE_URL

# Executar migrações
python manage.py migrate
```

## 🔄 Atualizações

### Deploy de Novas Versões

```bash
# Fazer alterações no código
git add .
git commit -m "feat: nova funcionalidade"
git push origin main

# Deploy automático será executado
```

### Migrações do Banco

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar em produção (automático via Procfile)
# ou manualmente:
railway run python manage.py migrate
```

## 📞 Suporte

### URLs Importantes

- **Aplicação:** `https://seu-app.railway.app`
- **Admin:** `https://seu-app.railway.app/admin/`
- **Upload TIPI:** `https://seu-app.railway.app/auditoria/upload-tipi-pdf/`

### Contatos

- **Documentação:** Este README
- **Logs:** Dashboard da plataforma
- **Suporte:** Suporte técnico da plataforma

---

## 🎯 Exemplo Completo - Railway

```bash
# 1. Preparar código
git add .
git commit -m "feat: sistema completo"
git push origin main

# 2. Acessar Railway
# railway.app -> Connect GitHub -> Select Repository

# 3. Configurar variáveis
DEBUG=false
SECRET_KEY=django-insecure-nova-chave-super-secreta
ALLOWED_HOSTS=.railway.app
DEEPSEEK_API_KEY=sk-sua-chave-deepseek

# 4. Deploy automático
# Railway detecta Procfile e faz deploy

# 5. Acessar aplicação
# https://fisco-auditoria.railway.app
```

**Tempo total:** ~10 minutos  
**Custo:** Gratuito por 30 dias, depois $5/mês  
**Resultado:** Sistema completo em produção com HTTPS! 🎉

---

**Versão:** 1.0  
**Data:** Janeiro 2025  
**Plataformas:** Railway, Render, Heroku  
**Compatibilidade:** Django 5.2.4, Python 3.13+ 