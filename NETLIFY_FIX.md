# 🔧 Correção do Erro de Dependências - Netlify

## ❌ Problema Original
```
Failed during stage 'Install dependencies': dependency_installation script returned non-zero exit code: 1
```

## ✅ Soluções Implementadas

### 1. **Build Mínimo e Robusto**
Criado `build-minimal.sh` que instala apenas dependências essenciais:

```bash
#!/bin/bash
echo "🚀 Build mínimo para Netlify"

# Instalar apenas o Django e WhiteNoise
pip install Django==5.1.4 whitenoise==6.6.0

# Criar diretório de estáticos
mkdir -p staticfiles

# Coletar arquivos estáticos
DJANGO_SETTINGS_MODULE=netlify_settings python manage.py collectstatic --noinput --clear

echo "✅ Build mínimo concluído!"
```

### 2. **Configurações Django Simplificadas**
Criado `netlify_settings.py` com configurações mínimas:

- ✅ Sem dependências problemáticas
- ✅ Configurações básicas do Django
- ✅ WhiteNoise para arquivos estáticos
- ✅ SQLite como banco de dados
- ✅ Configurações de segurança básicas

### 3. **Requirements Alternativos**
Criado `requirements-netlify.txt` com dependências testadas:

```txt
Django==5.1.4
gunicorn==21.2.0
whitenoise==6.6.0
python-decouple==3.8
dj-database-url==2.1.0
requests==2.31.0
pillow==10.2.0
beautifulsoup4==4.12.3
markdown==3.5.2
```

### 4. **Configuração Netlify Otimizada**
Atualizado `netlify.toml`:

```toml
[build]
  command = "./build-minimal.sh"
  publish = "staticfiles"

[build.environment]
  PYTHON_VERSION = "3.11"
  DJANGO_SETTINGS_MODULE = "netlify_settings"
  DEBUG = "False"
```

## 🚀 Como Aplicar as Correções

### Opção 1: Build Mínimo (Recomendado)
1. **Configure no Netlify**:
   - Build command: `./build-minimal.sh`
   - Publish directory: `staticfiles`
   - Environment: `DJANGO_SETTINGS_MODULE=netlify_settings`

2. **Variáveis de Ambiente**:
   ```env
   DJANGO_SETTINGS_MODULE=netlify_settings
   DEBUG=False
   SECRET_KEY=sua-chave-secreta-aqui
   ```

### Opção 2: Build com Requirements Alternativos
1. **Configure no Netlify**:
   - Build command: `./build-netlify.sh`
   - Publish directory: `staticfiles`

2. **O script usará** `requirements-netlify.txt` automaticamente

### Opção 3: Build Manual no Netlify
Se os scripts não funcionarem, configure manualmente:

1. **Build command**:
   ```bash
   pip install Django==5.1.4 whitenoise==6.6.0 && mkdir -p staticfiles && DJANGO_SETTINGS_MODULE=netlify_settings python manage.py collectstatic --noinput
   ```

2. **Publish directory**: `staticfiles`

## 🔍 Diagnóstico de Problemas

### Se ainda houver erro de dependências:
1. **Verifique os logs** completos do Netlify
2. **Teste localmente**:
   ```bash
   ./build-minimal.sh
   ```
3. **Use build manual** se necessário

### Se arquivos estáticos não carregarem:
1. **Verifique** se `staticfiles/` foi criado
2. **Confirme** que `DJANGO_SETTINGS_MODULE=netlify_settings`
3. **Teste** coleta local:
   ```bash
   DJANGO_SETTINGS_MODULE=netlify_settings python manage.py collectstatic
   ```

## 📊 Arquivos Criados/Modificados

- ✅ `build-minimal.sh` - Build mínimo e robusto
- ✅ `build-netlify.sh` - Build com requirements alternativos
- ✅ `netlify_settings.py` - Configurações Django simplificadas
- ✅ `requirements-netlify.txt` - Dependências testadas
- ✅ `netlify.toml` - Configuração otimizada
- ✅ `netlify-simple.toml` - Configuração alternativa

## 🎯 Próximos Passos

1. **Commit** todas as alterações
2. **Push** para o GitHub
3. **Trigger** novo build no Netlify
4. **Monitorar** logs do build
5. **Testar** site após deploy

## 📞 Se Ainda Houver Problemas

1. **Copie os logs completos** do Netlify
2. **Teste o build localmente**:
   ```bash
   ./build-minimal.sh
   ```
3. **Verifique** se todos os arquivos estão no repositório
4. **Use build manual** como último recurso

---

**✅ Essas correções devem resolver o erro de dependências no Netlify!** 