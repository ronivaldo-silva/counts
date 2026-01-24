# ✅ RESUMO: Configuração de Variáveis de Ambiente - Google Cloud

## 📦 O Que Foi Feito

### 1️⃣ **Arquivos Criados**

| Arquivo | Descrição |
|---------|-----------|
| `.env.example` | Template de variáveis de ambiente |
| `.gcloudignore` | Ignora arquivos no deploy GCloud |
| `deploy.ps1` | Script automatizado de deploy |
| `deploy-gcloud.md` | Guia completo de deploy manual |
| `app.yaml` | Config opcional App Engine |
| `GUIA-RAPIDO.md` | Este arquivo - resumo rápido |

### 2️⃣ **Arquivos Atualizados**

| Arquivo | Alteração |
|---------|-----------|
| `config.py` | ✅ Removida URL hardcoded (segurança)<br>✅ Lógica simplificada DATABASE_URL<br>✅ Suporte a `python-dotenv` |
| `requirements.txt` | ✅ Adicionado `python-dotenv>=1.0.0` |
| `README.md` | ✅ Seção de segurança atualizada<br>✅ Instruções de deploy Google Cloud |

---

## 🔑 Variáveis de Ambiente Configuradas

### Como Funciona Agora

```mermaid
graph TD
    A[Aplicação Inicia] --> B[load_dotenv carrega .env]
    B --> C{DATABASE_URL existe<br>no ambiente?}
    C -->|Sim| D[✅ Usa DATABASE_URL<br>do .env ou sistema]
    C -->|Não| E[✅ Usa LOCAL_DATABASE_URL<br>localhost:5432]
    D --> F[Conecta ao Banco]
    E --> F
    
    style D fill:#28a745,color:#fff
    style E fill:#ffc107,color:#000
    style F fill:#007bff,color:#fff
```

### Ordem de Prioridade (Simplificada)

```
1. DATABASE_URL (do arquivo .env ou variável de sistema)
   ↓ (se não existir)
2. LOCAL_DATABASE_URL (fallback - localhost - hardcoded no config.py)
```

**🔒 Mudança de Segurança Importante:**
- ❌ **REMOVIDO**: NEON_DATABASE_URL hardcoded do código
- ✅ **AGORA**: Todas as credenciais vivem APENAS no `.env`
- ✅ **BENEFÍCIO**: Zero risco de credenciais no repositório

---

## 🎯 Cenários de Uso

### 💻 Desenvolvimento Local

**Opção A: Usar arquivo `.env`**
```bash
# 1. Copiar template
cp .env.example .env

# 2. Editar .env
# Descomentar: DATABASE_URL=postgresql://userapp:Li0nt0g3ro!@localhost:5432/Counts

# 3. Rodar
poetry run flet run --web
```

**Opção B: Deixar automático**
```bash
# Sistema usa LOCAL_DATABASE_URL automaticamente
poetry run flet run --web
```

### ☁️ Google Cloud Run

**Deploy rápido:**
```powershell
./deploy.ps1
```

**O que acontece:**
1. ✅ Build da imagem Docker
2. ✅ Push para Google Container Registry
3. ✅ Deploy no Cloud Run
4. ✅ Cloud Run injeta `DATABASE_URL` automaticamente
5. ✅ Aplicação conecta ao Neon PostgreSQL

### 🌐 Render (Continua Funcionando)

Nada muda! O código é compatível:
```bash
# Render injeta DATABASE_URL
# Dockerfile existente funciona
```

---

## 📝 Checklist de Deploy

### Pré-Deploy

- [ ] Google Cloud SDK instalado (`gcloud --version`)
- [ ] Autenticado (`gcloud auth login`)
- [ ] Projeto selecionado (`gcloud config set project SEU-ID`)
- [ ] APIs habilitadas (Cloud Run + Cloud Build)

### Deploy

**Opção 1: Script Automatizado**
- [ ] Executar `./deploy.ps1`
- [ ] Selecionar projeto
- [ ] Configurar DATABASE_URL (Secret Manager ou direto)
- [ ] Aguardar build e deploy
- [ ] Copiar URL retornada

**Opção 2: Manual**
- [ ] Executar comando do `deploy-gcloud.md`
- [ ] Configurar variáveis de ambiente
- [ ] Verificar logs

### Pós-Deploy

- [ ] Acessar URL retornada
- [ ] Verificar logs (`gcloud run services logs tail`)
- [ ] Testar funcionalidades principais
- [ ] Configurar domínio personalizado (opcional)

---

## 🔧 Comandos Úteis

### Gerenciar Variáveis de Ambiente

```bash
# Ver variáveis configuradas
gcloud run services describe counts-app \
  --region southamerica-east1 \
  --format="value(spec.template.spec.containers[0].env)"

# Atualizar DATABASE_URL
gcloud run services update counts-app \
  --region southamerica-east1 \
  --set-env-vars DATABASE_URL="nova-url"

# Remover variável
gcloud run services update counts-app \
  --region southamerica-east1 \
  --remove-env-vars DATABASE_URL
```

### Secret Manager

```bash
# Criar secret
echo "postgresql://..." | gcloud secrets create database-url --data-file=-

# Atualizar secret
echo "nova-url" | gcloud secrets versions add database-url --data-file=-

# Usar secret no deploy
gcloud run services update counts-app \
  --update-secrets DATABASE_URL=database-url:latest

# Listar secrets
gcloud secrets list
```

### Monitoramento

```bash
# Logs em tempo real
gcloud run services logs tail counts-app --region southamerica-east1

# Últimos 50 logs
gcloud run services logs read counts-app \
  --region southamerica-east1 \
  --limit 50

# Status do serviço
gcloud run services describe counts-app --region southamerica-east1
```

---

## 🔒 Segurança

### ✅ Implementado

- ✅ `.env` no `.gitignore` - nunca commitado
- ✅ `.env` no `.dockerignore` - não vai para imagem Docker
- ✅ Suporte a Secret Manager
- ✅ SSL obrigatório no Neon (`sslmode=require`)
- ✅ HTTPS automático no Cloud Run
- ✅ **NOVO**: Credenciais removidas do código (agora só no .env)

### 🎯 Recomendações

1. **Use Secret Manager em produção:**
   ```bash
   # Ao invés de --set-env-vars
   --update-secrets DATABASE_URL=database-url:latest
   ```

2. **Nunca commite credenciais:**
   - ✅ Use `.env` local
   - ✅ Use Secret Manager na nuvem
   - ❌ Nunca hardcode passwords

3. **Rotacione senhas periodicamente:**
   ```bash
   # Atualizar secret
   gcloud secrets versions add database-url --data-file=-
   
   # Redesploy automático
   gcloud run services update counts-app \
     --update-secrets DATABASE_URL=database-url:latest
   ```

---

## 🆘 Problemas Comuns

### 1. "ModuleNotFoundError: No module named 'dotenv'"

**Solução:**
```bash
pip install python-dotenv
# ou
poetry add python-dotenv
```

### 2. "Connection to database failed"

**Diagnóstico:**
```bash
# 1. Verificar variável configurada
gcloud run services describe counts-app \
  --format="value(spec.template.spec.containers[0].env)"

# 2. Testar conexão local
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('DATABASE_URL'))"
```

### 3. "Permission denied on Google Cloud"

**Solução:**
```bash
# Habilitar APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Verificar permissões
gcloud projects get-iam-policy SEU-PROJETO-ID
```

### 4. ".env não está sendo lido"

**Verificações:**
1. ✅ Arquivo chamado exatamente `.env` (não `.env.txt`)
2. ✅ Arquivo na raiz do projeto
3. ✅ `python-dotenv` instalado
4. ✅ `load_dotenv()` sendo chamado

---

## 📊 Estrutura Final

```
Counts2/
├── .env                    # ❌ Não commitado - suas credenciais locais
├── .env.example            # ✅ Template commitado
├── .gitignore              # Ignora .env
├── .dockerignore           # Ignora .env no Docker
├── .gcloudignore           # Ignora arquivos no GCloud
├── Dockerfile              # Build da imagem
├── requirements.txt        # ✅ Incluindo python-dotenv
├── deploy.ps1              # Script de deploy
├── deploy-gcloud.md        # Guia completo
├── GUIA-RAPIDO.md          # Este arquivo
├── app.yaml                # App Engine (opcional)
├── README.md               # ✅ Atualizado
└── src/
    ├── main.py
    └── database/
        └── config.py       # ✅ Lógica de prioridade DATABASE_URL
```

---

## 🎓 Próximos Passos Sugeridos

1. **Deploy Inicial:**
   ```powershell
   ./deploy.ps1
   ```

2. **Configurar CI/CD (GitHub Actions):**
   - Deploy automático a cada push na main
   - Testes antes do deploy

3. **Configurar Domínio:**
   ```bash
   gcloud run domain-mappings create \
     --service counts-app \
     --domain seu-dominio.com
   ```

4. **Monitoramento:**
   - Configure alertas no Cloud Monitoring
   - Dashboard de métricas

5. **Backup Automatizado:**
   - Configure backup do Neon PostgreSQL
   - Plano de recuperação de desastres

---

## 📚 Documentação Adicional

- **Deploy Completo:** `deploy-gcloud.md`
- **README do Projeto:** `README.md`
- **Exemplo de .env:** `.env.example`

---

**✨ Tudo pronto! Seu projeto está configurado para multiple ambientes com Google Cloud!**

**Dúvidas?** Consulte `deploy-gcloud.md` para instruções detalhadas.
