# Guia de Deploy no Render - Counts2

Este guia descreve o processo passo-a-passo para hospedar o projeto **Counts2** na plataforma [Render](https://render.com/).

## Pré-requisitos
- Conta no GitHub com o código do projeto atualizado.
- Conta no Render.

## Passo 1: Preparar o Projeto (Já realizado)
Certifique-se de que os seguintes arquivos estão configurados corretamente (já fizemos isso para você):
- `requirements.txt`: Deve conter `flet` e dependências básicas. **Removemos FastAPI/Uvicorn para simplificar.**
- `src/main.py`: Configurado para rodar como aplicação Flet nativa.

## Passo 2: Criar Novo Web Service no Render
1. Acesse o [Dashboard do Render](https://dashboard.render.com/).
2. Clique no botão **"New +"** e selecione **"Web Service"**.
3. Selecione a opção **"Build and deploy from a Git repository"**.
4. Conecte sua conta do GitHub e escolha o repositório **Counts2**.

## Passo 3: Configurar o Serviço
Preencha os campos conforme abaixo:

| Campo | Valor |
|-------|-------|
| **Name** | `counts2-app` (ou o nome que preferir) |
| **Region** | Escolha a mais próxima (ex: Ohio, Oregon) |
| **Branch** | `main` (ou a branch que você está usando) |
| **Root Directory** | Deixe em branco (o padrão é a raiz) |
| **Runtime** | **Python 3** |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python src/main.py` |

> **Nota:** Certifique-se de selecionar o plano **Free** se for para testes.

## Passo 4: Variáveis de Ambiente (Environment Variables)
Role para baixo até a seção "Environment Variables" e adicione as seguintes:

1. **PYTHON_VERSION**
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0` (Para garantir compatibilidade)

2. **DATABASE_URL**
   - Key: `DATABASE_URL`
   - Value: `postgresql://counts_user:sjwE7n8IDkVuTfN9r8sruNHUueodvGet@dpg-d4tpaf6uk2gs73c40d00-a/counts_db`

3. **FLET_SECRET_KEY** (Recomendado)
   - Key: `FLET_SECRET_KEY`
   - Value: *Sua chave secreta aleatória*

## Passo 5: Finalizar e Fazer Deploy
1. Clique em **"Create Web Service"**.
2. Acompanhe os logs. O Render instalará as dependências e iniciará o servidor.
3. Quando ver "Live", acesse a URL da sua aplicação.

## Notas sobre Download de Recibos
- Os recibos gerados são salvos temporariamente em `storage/temp` para persistência.
- Para download, eles são disponibilizados via URL pública.
- Não é necessária configuração extra no Render para isso.
