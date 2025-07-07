# 🗄️ Guia de Importação de Dados - Railway

## 📊 Dados Exportados

✅ **Dados locais exportados com sucesso:**
- `usuarios.json` - 517 bytes (usuários e permissões)
- `dados_auditoria.json` - 12.9 MB (legislações, empresas, auditorias)

## 🚀 Métodos de Importação

### Método 1: Automático via Deploy (Recomendado)

Os dados serão importados automaticamente no próximo deploy:

1. **Arquivos já incluídos** no repositório
2. **Script automático** executará a importação
3. **Dados carregados** após o deploy

### Método 2: Railway CLI (Manual)

Se você tem o Railway CLI instalado:

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Fazer login
railway login

# Conectar ao projeto
railway link

# Executar comando de importação
railway run python manage.py importar_dados --tudo
```

### Método 3: Interface Web do Railway

1. **Acesse** o dashboard do Railway
2. **Vá para** "Deployments" → "Logs"
3. **Abra** o terminal web
4. **Execute** os comandos:
   ```bash
   python manage.py importar_dados --tudo
   ```

## 🔧 Comandos Disponíveis

### Importar Todos os Dados
```bash
python manage.py importar_dados --tudo
```

### Importar Apenas Usuários
```bash
python manage.py importar_dados --usuarios
```

### Importar Apenas Dados de Auditoria
```bash
python manage.py importar_dados --auditoria
```

## 📋 O que Será Importado

### 👥 Usuários (usuarios.json)
- Superusuários existentes
- Permissões e grupos
- Configurações de acesso

### 📊 Dados de Auditoria (dados_auditoria.json)
- **Legislações**: Todas as 104 legislações fiscais
- **Empresas**: Empresas cadastradas
- **Auditorias**: Histórico de auditorias
- **Documentos**: Metadados dos documentos

## 🎯 Verificação Pós-Importação

### 1. Verificar Admin
- Acesse: `https://seu-app.railway.app/admin/`
- Login: `admin` / `admin123`
- Verifique se os dados estão lá

### 2. Verificar Legislações
- Acesse: `https://seu-app.railway.app/auditoria/`
- Verifique se as 104 legislações estão carregadas
- Teste a funcionalidade de pesquisa

### 3. Verificar Empresas
- No admin, vá em "Empresas"
- Verifique se as empresas cadastradas estão lá
- Teste criação de nova empresa

## 🛠️ Troubleshooting

### Erro: "Arquivo não encontrado"
```bash
# Verificar se os arquivos estão no diretório correto
ls -la *.json

# Se não estiverem, baixar do repositório
wget https://raw.githubusercontent.com/Manoel1988/Fisco/main/usuarios.json
wget https://raw.githubusercontent.com/Manoel1988/Fisco/main/dados_auditoria.json
```

### Erro: "Violation of constraint"
```bash
# Limpar banco e reimportar
python manage.py flush --noinput
python manage.py migrate
python manage.py importar_dados --tudo
```

### Erro: "Permission denied"
```bash
# Verificar permissões
chmod +x setup-railway-data.sh
```

## 📊 Estrutura dos Dados

### Legislações Importadas
- **Lei Geral**: Lei 8.666/93, Lei 14.133/21
- **ICMS**: Regulamentos estaduais
- **ISS**: Leis municipais (Belo Horizonte)
- **Trabalhista**: CLT, Normas Regulamentadoras
- **Tributário**: CTN, Leis específicas

### Empresas Cadastradas
- Dados básicos (CNPJ, razão social)
- Configurações de auditoria
- Histórico de análises

## 🔄 Processo Automático

O sistema está configurado para:

1. **Detectar** arquivos JSON no deploy
2. **Executar** migrações automaticamente
3. **Importar** dados se disponíveis
4. **Criar** superusuário padrão
5. **Configurar** ambiente completo

## 📞 Próximos Passos

1. **Aguardar** próximo deploy (automático)
2. **Verificar** logs no Railway dashboard
3. **Testar** login no admin
4. **Confirmar** dados importados
5. **Usar** sistema normalmente

## 🎉 Resultado Esperado

Após a importação:
- ✅ **Admin funcional** com login
- ✅ **104 legislações** carregadas
- ✅ **Empresas** disponíveis
- ✅ **Histórico** de auditorias
- ✅ **Sistema completo** operacional

## 🔒 Credenciais

**Superusuário padrão:**
- **Usuário**: `admin`
- **Senha**: `admin123`
- **Email**: `admin@fisco.com`

⚠️ **Altere a senha** após primeiro login!

---

**🚀 Dados prontos para importação no Railway!** 