# Usar uma imagem base leve do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para Python
# Impede o Python de escrever arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que logs do Python sejam enviados direto para o terminal (logs do container)
ENV PYTHONUNBUFFERED=1

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte (pasta src)
COPY src/ ./src/

# Configurar a porta padrão (Google Cloud Run injeta a variável PORT, mas definimos um default)
ENV PORT=8080

# Expor a porta
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["python", "src/main.py"]
