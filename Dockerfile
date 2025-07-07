# Dockerfile otimizado para Railway - Sistema Fisco
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=railway_settings_minimal

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p staticfiles media logs

# Tornar script executável
RUN chmod +x start-railway-minimal.sh

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput --settings=railway_settings_minimal || echo "Static files collection failed, continuing..."

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["./start-railway-minimal.sh"] 