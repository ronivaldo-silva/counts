# Counts2 app

Sistema de gestão de contas desenvolvido com Flet e PostgreSQL.

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente

O projeto usa variáveis de ambiente para gerenciar credenciais com segurança:

1. **Copie o arquivo de exemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Configure DATABASE_URL no `.env`:**
   ```env
   # Para Neon Tech (Produção)
   DATABASE_URL=postgresql://seu-usuario:sua-senha@seu-host.neon.tech/seu-db?sslmode=require

   # OU para desenvolvimento local
   DATABASE_URL=postgresql://userapp:Li0nt0g3ro!@localhost:5432/Counts
   ```

**Ordem de Prioridade:**
1. `DATABASE_URL` do arquivo `.env` (desenvolvimento local)
2. `DATABASE_URL` injetada pelo Google Cloud/Render (produção)
3. `LOCAL_DATABASE_URL` (fallback hardcoded para localhost)

**🔒 Segurança:**
- ✅ Credenciais **NUNCA** estão no código
- ✅ `.env` está no `.gitignore` e `.dockerignore`
- ✅ Use Secret Manager no Google Cloud para produção

## 🚀 Deploy no Google Cloud

### Método Rápido (Script Automatizado)

```powershell
./deploy.ps1
```

O script irá guiá-lo através de:
- Seleção do projeto Google Cloud
- Configuração de variáveis de ambiente (Secret Manager ou direto)
- Build da imagem Docker
- Deploy no Cloud Run

### Método Manual

Consulte o guia completo em [`deploy-gcloud.md`](deploy-gcloud.md)

**Comandos Básicos:**
```bash
# Deploy rápido
gcloud run deploy counts-app \
  --source . \
  --platform managed \
  --region southamerica-east1 \
  --allow-unauthenticated

# Configurar variável de ambiente
gcloud run services update counts-app \
  --region southamerica-east1 \
  --set-env-vars DATABASE_URL="sua-database-url"
```

## 🏃 Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).