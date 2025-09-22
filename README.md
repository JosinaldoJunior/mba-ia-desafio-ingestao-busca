# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de busca e chat com IA baseado em RAG (Retrieval-Augmented Generation) usando PostgreSQL com extensão pgvector para armazenamento de embeddings.

## 📋 Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Conta OpenAI com API Key

## 🚀 Passo a Passo para Executar o Projeto

### 1. Configuração do Ambiente

#### 1.1 Clone o repositório e navegue até o diretório
```bash
cd mba-ia-desafio-ingestao-busca
```

#### 1.2 Crie um ambiente virtual Python
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

#### 1.3 Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configuração das Variáveis de Ambiente

#### 2.1 Crie um arquivo `.env` na raiz do projeto
```bash
touch .env
```

#### 2.2 Adicione as seguintes variáveis ao arquivo `.env`:
```env
# OpenAI Configuration
OPENAI_API_KEY=sua_chave_api_openai_aqui
OPENAI_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini

# Database Configuration
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=gpt5_collection

# PDF Configuration
PDF_PATH=../document.pdf
```

**⚠️ Importante:** Substitua `sua_chave_api_openai_aqui` pela sua chave real da OpenAI.

### 3. Configuração do Banco de Dados

#### 3.1 Inicie o PostgreSQL com pgvector usando Docker Compose
```bash
docker-compose up -d
```

#### 3.2 Aguarde o banco estar pronto
O comando acima irá:
- Iniciar o PostgreSQL na porta 5432
- Criar automaticamente a extensão `vector` necessária para embeddings
- Configurar o banco `rag` com usuário `postgres` e senha `postgres`

Você pode verificar se o banco está rodando com:
```bash
docker-compose ps
```

### 4. Ingestão de Dados

#### 4.1 Execute o script de ingestão
```bash
cd src
python ingest.py
```

Este script irá:
- Carregar o arquivo PDF (`document.pdf`)
- Dividir o documento em chunks de 1000 caracteres com overlap de 150
- Gerar embeddings usando o modelo `text-embedding-3-small`
- Armazenar os embeddings no PostgreSQL com pgvector

**✅ Sucesso:** Você verá a mensagem "Ingestion of documents finished with success"

### 5. Executar o Chat

#### 5.1 Inicie o sistema de chat
```bash
python chat.py
```

#### 5.2 Use o chat
- Digite suas perguntas sobre o conteúdo do documento
- O sistema buscará informações relevantes usando embeddings
- A IA responderá baseada apenas no conteúdo do documento
- Para sair, digite: `sair`, `quit`, `exit` ou `q`

### 6. Comandos Úteis

#### Parar o banco de dados
```bash
docker-compose down
```

#### Ver logs do banco
```bash
docker-compose logs postgres_rag_challenge
```

#### Limpar dados do banco (se necessário)
```bash
docker-compose down -v
docker-compose up -d
```

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Document  │───▶│   Text Splitter  │───▶│   Embeddings    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Vector Search   │◀───│  PostgreSQL +   │
└─────────────────┘    └──────────────────┘    │   pgvector      │
                                │               └─────────────────┘
                                ▼
                       ┌──────────────────┐
                       │   OpenAI GPT     │
                       │   (RAG Chain)    │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   AI Response    │
                       └──────────────────┘
```

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py          # Script de ingestão de dados
│   ├── search.py          # Sistema de busca vetorial
│   └── chat.py            # Interface de chat
├── document.pdf           # Documento para análise
├── docker-compose.yml     # Configuração do PostgreSQL
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🔧 Solução de Problemas

### Erro de conexão com o banco
- Verifique se o Docker está rodando: `docker ps`
- Verifique se o container está ativo: `docker-compose ps`
- Reinicie o banco: `docker-compose restart`

### Erro de API Key
- Verifique se a `OPENAI_API_KEY` está correta no arquivo `.env`
- Confirme se a chave tem créditos disponíveis na OpenAI

### Erro de ingestão
- Verifique se o arquivo `document.pdf` existe
- Confirme se o banco está rodando e acessível
- Verifique os logs: `docker-compose logs postgres_rag_challenge`

## 📝 Notas Técnicas

- **Modelo de Embedding:** `text-embedding-3-small` (padrão)
- **Modelo de Chat:** `gpt-4o-mini` (padrão)
- **Chunk Size:** 1000 caracteres
- **Chunk Overlap:** 150 caracteres
- **Similarity Search:** Top 3 documentos mais relevantes
- **Temperature:** 0.3 (para respostas mais consistentes)

## 🎯 Funcionalidades

- ✅ Ingestão automática de documentos PDF
- ✅ Busca semântica usando embeddings
- ✅ Chat interativo com IA
- ✅ Respostas baseadas apenas no conteúdo do documento
- ✅ Interface amigável no terminal
- ✅ Tratamento de erros robusto