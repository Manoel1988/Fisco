# Fisco - Sistema de Auditoria Fiscal

Sistema web desenvolvido em Django para auditoria fiscal com análise inteligente baseada em IA.

## Funcionalidades

- 📊 Auditoria fiscal automatizada
- 🤖 Análise inteligente com IA
- 📁 Upload e processamento de documentos fiscais
- 💰 Cálculo de valores de recuperação
- 📋 Relatórios detalhados de auditoria

## Tecnologias Utilizadas

- Python 3.x
- Django
- SQLite
- HTML/CSS/JavaScript
- Marked.js (para renderização de Markdown)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/fisco.git
cd fisco
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Inicie o servidor:
```bash
python manage.py runserver
```

## Uso

1. Acesse `http://localhost:8000/auditoria/`
2. Faça upload dos documentos fiscais
3. Execute a auditoria
4. Visualize os resultados da análise

## Estrutura do Projeto

```
Fisco/
├── auditoria/          # App principal de auditoria
├── core/              # Configurações do Django
├── media/             # Arquivos de upload
├── requirements.txt   # Dependências
└── manage.py         # Script de gerenciamento Django
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. 