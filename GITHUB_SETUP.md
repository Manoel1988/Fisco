# 🚀 Configuração do GitHub para o Projeto Fisco

## 📋 Passos para Configurar o Repositório no GitHub

### 1. Criar Repositório no GitHub
1. Acesse [GitHub](https://github.com)
2. Clique em "New repository" (botão verde)
3. Nome do repositório: `fisco`
4. Descrição: `Sistema de Auditoria Fiscal com IA`
5. **NÃO** marque "Initialize this repository with a README"
6. Clique em "Create repository"

### 2. Conectar seu Projeto Local ao GitHub
Após criar o repositório, execute os comandos abaixo no terminal:

```bash
# Adicionar o remote do GitHub (substitua SEU_USUARIO pelo seu nome de usuário)
git remote add origin https://github.com/SEU_USUARIO/fisco.git

# Fazer o primeiro push
git push -u origin main
```

### 3. Configurar Credenciais (se necessário)
Se for solicitado login, você pode:

**Opção A - Token de Acesso Pessoal (Recomendado):**
1. Vá em GitHub → Settings → Developer settings → Personal access tokens
2. Gere um novo token com permissões de `repo`
3. Use o token como senha quando solicitado

**Opção B - SSH (Mais Seguro):**
```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu-email@example.com"

# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar chave pública para GitHub
cat ~/.ssh/id_ed25519.pub

# Adicionar no GitHub: Settings → SSH and GPG keys → New SSH key
```

## 🔄 Automatização Configurada

### Push Automático
✅ **Hook post-commit ativado**: Toda vez que você fizer um commit, o código será automaticamente enviado para o GitHub!

### Script de Deploy Manual
✅ **Script `deploy.sh` criado**: Para fazer commit e push de uma vez:

```bash
./deploy.sh "Sua mensagem de commit"
```

## 🛠️ Como Usar

### Para Modificações Normais:
```bash
# Fazer suas modificações nos arquivos...

# Commit (irá fazer push automático)
git add .
git commit -m "Descrição das mudanças"
```

### Para Deploy Rápido:
```bash
# Fazer suas modificações nos arquivos...

# Deploy com uma linha
./deploy.sh "Descrição das mudanças"
```

## 📊 Status do Projeto

- ✅ Git inicializado
- ✅ .gitignore configurado
- ✅ README.md criado
- ✅ Primeiro commit realizado
- ✅ Hook de push automático configurado
- ✅ Script de deploy criado
- ⏳ Aguardando configuração do remote GitHub

## 🔧 Comandos Úteis

```bash
# Ver status do repositório
git status

# Ver histórico de commits
git log --oneline

# Ver remotes configurados
git remote -v

# Desabilitar push automático (se necessário)
chmod -x .git/hooks/post-commit

# Reabilitar push automático
chmod +x .git/hooks/post-commit
```

## 🆘 Solução de Problemas

### Erro de Autenticação
- Verifique se o token/senha está correto
- Considere usar SSH ao invés de HTTPS

### Push Automático Não Funciona
- Verifique se o hook está executável: `ls -la .git/hooks/post-commit`
- Verifique se o remote está configurado: `git remote -v`

### Conflitos de Merge
```bash
# Se houver conflitos, resolva manualmente e depois:
git add .
git commit -m "Resolve conflicts"
```

---

**📞 Suporte**: Se precisar de ajuda, verifique se seguiu todos os passos ou consulte a documentação do GitHub. 