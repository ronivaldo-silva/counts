# 🚀 Deploy no Google Cloud Run

## Pré-requisitos

1. **Google Cloud SDK instalado**
   ```bash
   # Windows: baixar de https://cloud.google.com/sdk/docs/install
   # Verificar instalação:
   gcloud --version
   ```

2. **Autenticação**
   ```bash
   gcloud auth login
   gcloud config set project SEU-PROJETO-ID
   ```

## Método 1: Deploy com Docker (Recomendado)

### Passo 1: Build e Push da Imagem

```bash
# Definir variáveis
$PROJECT_ID = "seu-projeto-id"
$SERVICE_NAME = "counts-app"
$REGION = "southamerica-east1"

# Build da imagem
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# OU usando Artifact Registry (mais moderno):
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/counts/$SERVICE_NAME
```

### Passo 2: Deploy no Cloud Run

```bash
# Deploy básico
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --set-env-vars DATABASE_URL="postgresql://neondb_owner:npg_ajvtGH2FU3ri@ep-divine-shadow-acn5sul1-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

### Passo 3: Deploy com SECRET (Mais Seguro)

```bash
# 1. Criar secret no Secret Manager
gcloud secrets create database-url `
  --data-file=- <<< "postgresql://neondb_owner:npg_ajvtGH2FU3ri@ep-divine-shadow-acn5sul1-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 2. Deploy usando secret
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --update-secrets DATABASE_URL=database-url:latest
```

## Método 2: Deploy direto do código (sem Docker)

```bash
gcloud run deploy $SERVICE_NAME `
  --source . `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --set-env-vars DATABASE_URL="sua-database-url-aqui"
```

## Configurações Avançadas

### Ajustar recursos

```bash
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --memory 512Mi `
  --cpu 1 `
  --timeout 300 `
  --concurrency 80 `
  --min-instances 0 `
  --max-instances 5
```

### Configurar domínio personalizado

```bash
# 1. Mapear domínio
gcloud run domain-mappings create `
  --service $SERVICE_NAME `
  --domain seu-dominio.com `
  --region $REGION

# 2. Seguir instruções para configurar DNS
```

## Verificar Deploy

```bash
# Ver logs
gcloud run services logs read $SERVICE_NAME --region $REGION

# Ver detalhes do serviço
gcloud run services describe $SERVICE_NAME --region $REGION

# Listar serviços
gcloud run services list
```

## Atualizar Variáveis de Ambiente

```bash
# Atualizar DATABASE_URL
gcloud run services update $SERVICE_NAME `
  --region $REGION `
  --set-env-vars DATABASE_URL="nova-url-aqui"

# Ou usar secrets
gcloud run services update $SERVICE_NAME `
  --region $REGION `
  --update-secrets DATABASE_URL=database-url:latest
```

## Rollback

```bash
# Listar revisões
gcloud run revisions list --service $SERVICE_NAME --region $REGION

# Fazer rollback para revisão anterior
gcloud run services update-traffic $SERVICE_NAME `
  --region $REGION `
  --to-revisions REVISION-NAME=100
```

## Deletar Serviço

```bash
gcloud run services delete $SERVICE_NAME --region $REGION
```

## Troubleshooting

### Logs em tempo real
```bash
gcloud run services logs tail $SERVICE_NAME --region $REGION
```

### Testar localmente com Docker
```bash
# Build local
docker build -t counts-app .

# Run local
docker run -p 8080:8080 `
  -e DATABASE_URL="sua-database-url-aqui" `
  counts-app
```

### Ver variáveis de ambiente configuradas
```bash
gcloud run services describe $SERVICE_NAME `
  --region $REGION `
  --format "value(spec.template.spec.containers[0].env)"
```

## Notas Importantes

1. ✅ **Secrets vs Variáveis**: Use Secret Manager para dados sensíveis (DATABASE_URL)
2. ✅ **Região**: `southamerica-east1` (São Paulo) tem menor latência no Brasil
3. ✅ **Cold Start**: Configure `min-instances` > 0 para evitar cold starts
4. ✅ **Custos**: Com `min-instances: 0`, você paga apenas pelo uso
5. ✅ **SSL**: Cloud Run fornece HTTPS automaticamente

## Links Úteis

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Secret Manager](https://cloud.google.com/secret-manager/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
