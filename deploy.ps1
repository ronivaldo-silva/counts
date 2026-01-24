# ========================================
# SCRIPT DE DEPLOY GOOGLE CLOUD RUN
# ========================================
# Execute este script para fazer deploy no Google Cloud Run

param(
    [string]$ProjectId = "",
    [string]$ServiceName = "counts-app",
    [string]$Region = "southamerica-east1"
)

# Cores para output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "========================================="
Write-Info "   DEPLOY COUNTS APP - GOOGLE CLOUD RUN"
Write-Info "========================================="
Write-Host ""

# Verificar se gcloud está instalado
Write-Info "🔍 Verificando Google Cloud SDK..."
try {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Success "✅ Google Cloud SDK instalado: $gcloudVersion"
} catch {
    Write-Error "❌ Google Cloud SDK não encontrado!"
    Write-Warning "Instale em: https://cloud.google.com/sdk/docs/install"
    exit 1
}
Write-Host ""

# Solicitar Project ID se não fornecido
if ([string]::IsNullOrEmpty($ProjectId)) {
    Write-Info "📋 Projetos disponíveis:"
    gcloud projects list --format="table(projectId,name)"
    Write-Host ""
    $ProjectId = Read-Host "Digite o Project ID"
}

# Configurar projeto
Write-Info "🔧 Configurando projeto: $ProjectId"
gcloud config set project $ProjectId
Write-Host ""

# Confirmar dados
Write-Info "📝 Configuração do Deploy:"
Write-Host "   • Projeto: $ProjectId"
Write-Host "   • Serviço: $ServiceName"
Write-Host "   • Região: $Region"
Write-Host ""

$confirm = Read-Host "Deseja continuar com o deploy? (s/n)"
if ($confirm -ne "s" -and $confirm -ne "S") {
    Write-Warning "Deploy cancelado."
    exit 0
}
Write-Host ""

# Perguntar sobre uso de Secret Manager
Write-Info "🔐 Gerenciamento de Variáveis de Ambiente"
Write-Host "Escolha uma opção:"
Write-Host "  1 - Usar Secret Manager (Recomendado - mais seguro)"
Write-Host "  2 - Usar variável de ambiente direta"
Write-Host "  3 - Usar .env.example padrão (Neon Tech)"
$secretChoice = Read-Host "Opção"

$envVars = ""
$secretArgs = ""

switch ($secretChoice) {
    "1" {
        Write-Info "📦 Configurando Secret Manager..."
        $dbUrl = Read-Host "Digite a DATABASE_URL (será armazenada com segurança)"
        
        # Criar secret
        Write-Info "Criando secret 'database-url'..."
        echo $dbUrl | gcloud secrets create database-url --data-file=- 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Secret já existe, atualizando..."
            echo $dbUrl | gcloud secrets versions add database-url --data-file=-
        }
        
        $secretArgs = "--update-secrets=DATABASE_URL=database-url:latest"
        Write-Success "✅ Secret configurado!"
    }
    "2" {
        $dbUrl = Read-Host "Digite a DATABASE_URL"
        $envVars = "--set-env-vars=DATABASE_URL=$dbUrl"
    }
    "3" {
        # Usar Neon Tech do .env.example
        $neonUrl = "postgresql://neondb_owner:npg_ajvtGH2FU3ri@ep-divine-shadow-acn5sul1-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        $envVars = "--set-env-vars=DATABASE_URL=$neonUrl"
        Write-Success "✅ Usando Neon Tech URL padrão"
    }
}
Write-Host ""

# Build da imagem
Write-Info "🏗️  Fazendo build da imagem Docker..."
Write-Host "Isso pode levar alguns minutos..."
Write-Host ""

$imageUri = "gcr.io/$ProjectId/$ServiceName"
gcloud builds submit --tag $imageUri

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Erro no build da imagem!"
    exit 1
}
Write-Success "✅ Build concluído com sucesso!"
Write-Host ""

# Deploy no Cloud Run
Write-Info "🚀 Fazendo deploy no Cloud Run..."
Write-Host ""

$deployCmd = "gcloud run deploy $ServiceName --image $imageUri --platform managed --region $Region --allow-unauthenticated --memory 512Mi --cpu 1 --timeout 300"

if (![string]::IsNullOrEmpty($envVars)) {
    $deployCmd += " $envVars"
}
if (![string]::IsNullOrEmpty($secretArgs)) {
    $deployCmd += " $secretArgs"
}

Invoke-Expression $deployCmd

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Erro no deploy!"
    exit 1
}
Write-Host ""

# Obter URL do serviço
Write-Success "✨ Deploy concluído com sucesso!"
Write-Host ""
Write-Info "📍 Obtendo URL do serviço..."
$serviceUrl = gcloud run services describe $ServiceName --region $Region --format="value(status.url)"

Write-Host ""
Write-Success "========================================="
Write-Success "   ✅ DEPLOY CONCLUÍDO COM SUCESSO!"
Write-Success "========================================="
Write-Host ""
Write-Info "🌐 URL do serviço: $serviceUrl"
Write-Host ""
Write-Info "📚 Comandos úteis:"
Write-Host "   • Ver logs:    gcloud run services logs tail $ServiceName --region $Region"
Write-Host "   • Detalhes:    gcloud run services describe $ServiceName --region $Region"
Write-Host "   • Deletar:     gcloud run services delete $ServiceName --region $Region"
Write-Host ""
Write-Success "🎉 Aplicação disponível em: $serviceUrl"
