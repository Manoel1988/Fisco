# 🏛️ Sistema Fisco - Auditoria Fiscal Inteligente

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema completo de auditoria fiscal com inteligência artificial para análise de documentos fiscais brasileiros.

## 🚀 Características Principais

- **🤖 Inteligência Artificial**: Integração com DeepSeek para análise inteligente de documentos
- **📚 Base Legal Completa**: 104 legislações fiscais com texto completo
- **🔍 Tabela TIPI 2024**: Classificação fiscal oficial completa
- **📄 Upload de Documentos**: Sistema seguro de upload e validação
- **🔐 Segurança Enterprise**: Configurações de segurança para produção
- **⚡ Performance Otimizada**: Consultas otimizadas com índices de banco
- **🧪 Testes Automatizados**: Cobertura completa de testes
- **📊 Interface Administrativa**: Django Admin configurado e otimizado

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.1, Python 3.13
- **Banco de Dados**: SQLite (incluso com dados)
- **IA**: DeepSeek API para análise de documentos
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Testes**: Django TestCase, Coverage
- **Deploy**: Docker, Railway, Render

## 📦 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/Manoel1988/Fisco.git
cd Fisco
```

### 2. Crie o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Execute o Sistema
```bash
python manage.py runserver
```

🎉 **Pronto!** O sistema estará rodando em `http://localhost:8000`

## 🔑 Configuração da API

Para usar a análise com IA, configure sua chave da API DeepSeek no arquivo `.env`:

```env
DEEPSEEK_API_KEY=sua_chave_aqui
```

## 📊 Dados Inclusos

O repositório já inclui:

- **✅ Banco de dados completo** com 104 legislações fiscais
- **✅ Tabela TIPI 2024** oficial
- **✅ Dados de empresas** para teste
- **✅ Documentos fiscais** de exemplo
- **✅ Usuário admin** (admin/admin123)

## 🏗️ Estrutura do Projeto

```
Fisco/
├── auditoria/              # App principal de auditoria
│   ├── management/         # Comandos Django personalizados
│   ├── migrations/         # Migrações do banco de dados
│   ├── templates/          # Templates HTML
│   └── ...
├── core/                   # Configurações do Django
├── media/                  # Arquivos de upload
├── staticfiles/            # Arquivos estáticos
├── db.sqlite3              # Banco de dados (incluso)
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🔧 Comandos Úteis

### Executar Testes
```bash
python manage.py test
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Carregar Dados de Exemplo
```bash
python manage.py demo_legislacoes
```

### Atualizar Legislações
```bash
python manage.py carregar_legislacoes_completas
```

## 🌐 Deploy

O sistema está pronto para deploy em:

- **Netlify**: `netlify.toml` e `build.sh` configurados
- **Railway**: `railway.toml` configurado
- **Render**: `render.yaml` configurado
- **Docker**: `Dockerfile` e `docker-compose.yml`
- **Heroku**: `Procfile` configurado

### Deploy Automático
```bash
chmod +x deploy.sh
./deploy.sh
```

## 📈 Funcionalidades

### 🏢 Gestão de Empresas
- Cadastro completo de empresas
- Dados fiscais e tributários
- Histórico de auditoria

### 📄 Documentos Fiscais
- Upload seguro de documentos
- Validação de tipos e tamanhos
- Análise automática com IA

### 📚 Base Legal
- 104 legislações fiscais completas
- Busca avançada por texto
- Classificação por esfera e órgão

### 🔍 Tabela TIPI
- Classificação fiscal oficial 2024
- Busca por código NCM
- Alíquotas e descrições

### 🤖 Análise Inteligente
- Detecção de inconsistências
- Sugestões de correção
- Relatórios automáticos

## 🔒 Segurança

- Validação de uploads
- Proteção CSRF
- Headers de segurança
- Sanitização de dados
- Logs de auditoria

## 📊 Estatísticas do Sistema

- **227 arquivos** no repositório
- **48 arquivos Python** de código
- **104 legislações** fiscais completas
- **7.983.042 caracteres** de conteúdo legal
- **155 commits** de desenvolvimento
- **32.022 linhas** de código adicionadas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Documentação

- [Guia de Legislações](GUIA_LEGISLACOES.md)
- [Relatório de Problemas Resolvidos](RELATORIO_PROBLEMAS_RESOLVIDOS.md)
- [Guia de Deploy](README_DEPLOY.md)

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma [Issue](https://github.com/Manoel1988/Fisco/issues)
- Consulte a [Documentação](https://github.com/Manoel1988/Fisco/wiki)

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido com ❤️ para facilitar a auditoria fiscal brasileira** 