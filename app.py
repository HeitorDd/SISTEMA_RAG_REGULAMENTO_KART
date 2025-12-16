import streamlit as st
import os
from dotenv import load_dotenv
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Importa a função para recriar o banco de dados
from criar_db import criar_db

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
CAMINHO_DATABASE = "database"
MODELO_EMBEDDING = "models/text-embedding-004"
MODELO_LLM = "gemini-2.5-flash-lite"

# Configuração da Página
st.set_page_config(page_title="Assistente de Kart", page_icon="🏎️", layout="centered")

st.title("🏎️ Assistente de Regulamento de Kart")
st.markdown("Tire suas dúvidas sobre o regulamento técnico e desportivo.")

# Sidebar com opções
with st.sidebar:
    st.header("Administração")
    st.markdown("Use o botão abaixo caso tenha adicionado novos PDFs na pasta `base`.")
    if st.button("🔄 Recriar Banco de Dados"):
        with st.spinner("Processando documentos e criando banco de dados..."):
            try:
                criar_db()
                st.success("Banco de dados atualizado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao criar banco de dados: {e}")

# Template do Prompt (Mesmo do main.py)
prompt_template_kart = """
Você é um assistente de IA especializado e rigoroso em regulamentos de competições de Kart.
Sua missão é responder dúvidas de pilotos e equipes com base EXCLUSIVAMENTE nas regras fornecidas.

Siga estas diretrizes estritamente:
1. **Fundamentação:** Sempre cite o artigo, parágrafo ou seção do regulamento que justifica sua resposta (ex: "Conforme Artigo 5.2...").
2. **Precisão Técnica:** Mantenha a terminologia técnica correta (ex: bandeiras, pesos, medidas, punições).
3. **Honestidade:** Se a resposta para a pergunta não estiver contida no texto abaixo, diga: "Não encontrei essa informação específica no trecho do regulamento fornecido." Não invente regras.

---
TRECHO DO REGULAMENTO (BASE DE CONHECIMENTO):
{base_conhecimento}
---

PERGUNTA DO USUÁRIO:
{pergunta}

RESPOSTA:
"""

# Inicializar histórico de chat na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta sobre o regulamento..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processar resposta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if not os.path.exists(CAMINHO_DATABASE):
            response = "⚠️ O banco de dados não foi encontrado. Por favor, clique em 'Recriar Banco de Dados' na barra lateral."
            message_placeholder.markdown(response)
        else:
            try:
                with st.spinner("Consultando o regulamento..."):
                    embedding_function = GoogleGenerativeAIEmbeddings(model=MODELO_EMBEDDING)
                    db = Chroma(persist_directory=CAMINHO_DATABASE, embedding_function=embedding_function)
                    
                    # Busca por similaridade
                    resultados = db.similarity_search_with_relevance_scores(prompt, k=3)
                    
                    if not resultados or resultados[0][1] < 0.3:
                        response = "Não consegui encontrar informações relevantes no regulamento para responder sua pergunta."
                    else:
                        textos_resultado = [res[0].page_content for res in resultados]
                        base_conhecimento = "\n\n----\n\n".join(textos_resultado)
                        
                        llm = ChatGoogleGenerativeAI(model=MODELO_LLM)
                        chain = PromptTemplate.from_template(prompt_template_kart) | llm
                        response = chain.invoke({"base_conhecimento": base_conhecimento, "pergunta": prompt}).content
                    
                    message_placeholder.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")