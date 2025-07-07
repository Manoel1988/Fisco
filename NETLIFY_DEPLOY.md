# 🌐 Deploy no Netlify - Sistema Fisco

Este guia explica como fazer deploy do Sistema Fisco no Netlify após as correções aplicadas.

## 🔧 Correções Aplicadas

### ✅ Problema Python 3.13 Resolvido

O erro original era:
```
python-build: definition not found: python-3.13.1
```

**Soluções implementadas:**

1. **Versão do Python alterada**: `runtime.txt` agora usa `python-3.11.9`
2. **Arquivo .python-version**: Criado para especificar versão compatível
3. **Configuração Netlify**: `netlify.toml` com configurações específicas
4. **Script de build**: `build.sh` personalizado para o processo de build
5. **Redirects**: Arquivo `_redirects` para roteamento correto

## 📦 Arquivos de Configuração

### `runtime.txt`
```
python-3.11.9
```

### `.python-version`
```
3.11.9
```

### `netlify.toml`
```toml
[build]
  command = "./build.sh"
  publish = "staticfiles"

[build.environment]
  PYTHON_VERSION = "3.11"
  DJANGO_SETTINGS_MODULE = "core.settings"
  DEBUG = "False"
  ALLOWED_HOSTS = "*.netlify.app"
```

### `build.sh`
Script personalizado que:
- Instala dependências
- Cria diretório de logs
- Coleta arquivos estáticos
- Executa migrações
- Prepara sistema para produção

## 🚀 Como Fazer Deploy

### 1. Conectar Repositório
1. Acesse [Netlify](https://netlify.com)
2. Faça login na sua conta
3. Clique em "New site from Git"
4. Conecte seu repositório GitHub: `https://github.com/Manoel1988/Fisco`

### 2. Configurar Build
O Netlify detectará automaticamente as configurações do `netlify.toml`:
- **Build command**: `./build.sh`
- **Publish directory**: `staticfiles`
- **Python version**: `3.11`

### 3. Variáveis de Ambiente
Configure as seguintes variáveis no painel do Netlify:

```env
DEBUG=False
SECRET_KEY=sua-chave-secreta-aqui
DEEPSEEK_API_KEY=sua-chave-deepseek-aqui
ALLOWED_HOSTS=*.netlify.app
DJANGO_SETTINGS_MODULE=core.settings
```

### 4. Deploy
1. Clique em "Deploy site"
2. Aguarde o processo de build
3. Acesse sua URL do Netlify

## 🔍 Verificação do Deploy

Após o deploy, verifique:

1. **✅ Site carregando**: Acesse a URL fornecida pelo Netlify
2. **✅ Admin funcionando**: `/admin/` deve carregar corretamente
3. **✅ Arquivos estáticos**: CSS e JS devem estar funcionando
4. **✅ Upload de arquivos**: Teste a funcionalidade de upload

## 🛠️ Troubleshooting

### Erro de Python Version
Se ainda houver erro de versão do Python:
1. Verifique se `runtime.txt` tem `python-3.11.9`
2. Confirme que `.python-version` existe com `3.11.9`
3. Limpe o cache do Netlify e refaça o deploy

### Erro de Static Files
Se arquivos estáticos não carregarem:
1. Verifique se `build.sh` está executável
2. Confirme que `staticfiles` está sendo gerado
3. Verifique configurações de `STATIC_ROOT` no Django

### Erro de Database
Se houver erro de banco de dados:
1. Verifique se `db.sqlite3` está no repositório
2. Confirme que migrações estão sendo executadas
3. Verifique logs do Netlify para erros específicos

## 📊 Recursos do Sistema no Netlify

Após deploy bem-sucedido, você terá:

- **🏛️ Sistema completo** de auditoria fiscal
- **📚 104 legislações** fiscais carregadas
- **🔍 Tabela TIPI 2024** funcional
- **🤖 Análise com IA** (configure API key)
- **🔐 Admin Django** para gestão
- **📄 Upload de documentos** funcionando

## 🌐 URLs Importantes

Após deploy:
- **Site principal**: `https://seu-site.netlify.app/`
- **Admin**: `https://seu-site.netlify.app/admin/`
- **Auditoria**: `https://seu-site.netlify.app/auditoria/`

## 📞 Suporte

Se encontrar problemas:
1. Verifique logs do Netlify
2. Consulte [documentação do Netlify](https://docs.netlify.com/)
3. Abra issue no repositório GitHub

---

**✅ Sistema Fisco pronto para produção no Netlify!** 