import os
from pathlib import Path
import re
from dotenv import load_dotenv
from typing import Dict, Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate

load_dotenv()

for k in ("OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

# Configurações
embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL", "text-embedding-3-small"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
)

# Função para buscar documentos
def search_documents(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Busca documentos relevantes no banco vetorial"""
    query = inputs["query"]
    k = inputs.get("k", 10)
    
    results = store.similarity_search_with_score(query=query, k=k)
    documents = [doc for doc, score in results]
    
    # Formatar contexto
    context_parts = []
    for i, doc in enumerate(documents, 1):
        context_parts.append(f"Documento {i}:\n{doc.page_content.strip()}\n")
    
    context = "\n".join(context_parts)
    
    return {
        "query": query,
        "context": context,
        "documents": documents
    }

def search_prompt(question=None):
   
    PROMPT_TEMPLATE = PromptTemplate(
      input_variables=["context", "query"],
      template="""
        CONTEXTO:
        {context}

        REGRAS:
        - Responda somente com base no CONTEXTO.
        - Se a informação não estiver explicitamente no CONTEXTO, responda:
          "Não tenho informações necessárias para responder sua pergunta."
        - Nunca invente ou use conhecimento externo.
        - Nunca produza opiniões ou interpretações além do que está escrito.

        EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
        Pergunta: "Qual é a capital da França?"
        Resposta: "Não tenho informações necessárias para responder sua pergunta."

        Pergunta: "Quantos clientes temos em 2024?"
        Resposta: "Não tenho informações necessárias para responder sua pergunta."

        Pergunta: "Você acha isso bom ou ruim?"
        Resposta: "Não tenho informações necessárias para responder sua pergunta."

        PERGUNTA DO USUÁRIO:
        {query}

        RESPONDA A "PERGUNTA DO USUÁRIO"
        """
        )

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano"),
        temperature=0.3
    )

    # Criar a chain usando pipe operator (seguindo o padrão do projeto)
    search_chain = RunnableLambda(search_documents)
    llm_chain = PROMPT_TEMPLATE | llm

    # Chain completa
    full_chain = search_chain | llm_chain

    query = question

    try:
        return full_chain.invoke({"query": query, "k": 3})
    except Exception as e:
        print(f"❌ Erro ao realizar busca, tente novamente mais tarde. {e}")
