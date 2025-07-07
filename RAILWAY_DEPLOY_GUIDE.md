# 🚂 Guia de Deploy no Railway - Sistema Fisco

## 🔧 Correções Implementadas

### ✅ Problemas Comuns Resolvidos:

1. **Configuração railway.toml otimizada**
2. **Script de inicialização personalizado**
3. **Configurações Django específicas**
4. **Suporte a PostgreSQL e SQLite**
5. **Variáveis de ambiente configuradas**

## 📦 Arquivos Criados/Atualizados

### 1. `railway.toml` (Configuração Principal)
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "./start-railway.sh"
healthcheckPath = "/"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[variables]
DJANGO_SETTINGS_MODULE = "railway_settings"
DEBUG = "False"
PYTHONUNBUFFERED = "1"
PORT = "8000"
```

### 2. `start-railway.sh` (Script de Inicialização)
- ✅ Executa migrações automaticamente
- ✅ Coleta arquivos estáticos
- ✅ Cria superusuário padrão
- ✅ Inicia Gunicorn com configurações otimizadas

### 3. `railway_settings.py` (Configurações Django)
- ✅ Hosts do Railway configurados
- ✅ Suporte a PostgreSQL e SQLite
- ✅ Configurações de segurança
- ✅ Logging otimizado

### 4. `nixpacks.toml` (Configuração de Build)
- ✅ Python 3.9 configurado
- ✅ Instalação de dependências
- ✅ Build automatizado

## 🚀 Como Fazer Deploy

### Opção 1: Deploy Direto pelo GitHub

1. **Acesse** [railway.app](https://railway.app)
2. **Faça login** com GitHub
3. **Clique** em "New Project"
4. **Selecione** "Deploy from GitHub repo"
5. **Escolha** o repositório `Manoel1988/Fisco`
6. **Configure** variáveis de ambiente (opcional):
   ```env
   SECRET_KEY=sua-chave-secreta-aqui
   DEEPSEEK_API_KEY=sua-chave-deepseek
   DEBUG=False
   ```

### Opção 2: Deploy via Railway CLI

1. **Instale** Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. **Faça login**:
   ```bash
   railway login
   ```

3. **Inicialize** projeto:
   ```bash
   railway init
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

## 🔍 Verificação Pós-Deploy

Após o deploy, verifique:

1. **✅ Site carregando**: Acesse a URL fornecida pelo Railway
2. **✅ Admin funcionando**: `/admin/` deve carregar
3. **✅ Login**: Use `admin/admin123` (criado automaticamente)
4. **✅ Arquivos estáticos**: CSS e JS carregando
5. **✅ Upload**: Teste funcionalidade de upload

## 🛠️ Troubleshooting

### Erro de Build
Se o build falhar:
1. **Verifique** logs no Railway dashboard
2. **Confirme** que `start-railway.sh` está executável
3. **Teste** localmente:
   ```bash
   chmod +x start-railway.sh
   ./start-railway.sh
   ```

### Erro de Dependências
Se houver erro com requirements:
1. **Verifique** `requirements.txt`
2. **Use** versões específicas:
   ```txt
   Django==5.1.4
   gunicorn==21.2.0
   whitenoise==6.6.0
   ```

### Erro de Database
Se houver erro de banco:
1. **Railway** pode fornecer PostgreSQL automaticamente
2. **Verifique** variável `DATABASE_URL`
3. **SQLite** funciona como fallback

### Erro de Static Files
Se arquivos estáticos não carregarem:
1. **Verifique** se `collectstatic` executou
2. **Confirme** configurações de `STATIC_ROOT`
3. **WhiteNoise** deve estar configurado

## 📊 Configurações Recomendadas

### Variáveis de Ambiente no Railway:
```env
DJANGO_SETTINGS_MODULE=railway_settings
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-longa-e-segura
DEEPSEEK_API_KEY=sua-chave-deepseek-para-ia
PYTHONUNBUFFERED=1
```

### Recursos Recomendados:
- **CPU**: 1 vCPU (suficiente para início)
- **RAM**: 512MB (mínimo recomendado)
- **Storage**: 1GB (para arquivos e banco)

## 🔗 URLs Importantes

Após deploy bem-sucedido:
- **Site**: `https://seu-app.railway.app/`
- **Admin**: `https://seu-app.railway.app/admin/`
- **API**: `https://seu-app.railway.app/auditoria/`

## 🎯 Credenciais Padrão

O sistema cria automaticamente:
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Email**: `admin@example.com`

⚠️ **IMPORTANTE**: Altere a senha após primeiro login!

## 📞 Suporte

Se ainda houver problemas:

1. **Verifique logs** no Railway dashboard
2. **Teste configurações** localmente
3. **Consulte** [documentação do Railway](https://docs.railway.app/)
4. **Abra issue** no GitHub se necessário

## 🏆 Vantagens do Railway

- ✅ **Deploy automático** via GitHub
- ✅ **PostgreSQL gratuito** incluído
- ✅ **HTTPS automático**
- ✅ **Logs em tempo real**
- ✅ **Escalabilidade automática**
- ✅ **Rollback fácil**

---

**🎉 Sistema Fisco pronto para produção no Railway!** 