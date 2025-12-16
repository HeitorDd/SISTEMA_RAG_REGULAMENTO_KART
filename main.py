from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
# from langchain.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

CAMINHO_DATABASE = "database"

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
def perguntar():
    funcao_embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    #carregar banco de dados
    db = Chroma(persist_directory = CAMINHO_DATABASE, embedding_function = funcao_embedding)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    prompt = PromptTemplate.from_template(prompt_template_kart)
    chain = prompt | llm

    while True:
        pergunta = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if pergunta.lower() in ['sair', 'exit']:
            break

        #comparar pergunta vetorizzada com banco de dados vetorizado
        resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)
        
        # Debug: Imprimir scores para verificar a calibração
        if resultados:
            print(f"Top score encontrado: {resultados[0][1]}")

        if len(resultados) == 0 or resultados[0][1] < 0.3:
            print("Não conseguiu encontrar alguma informação relevante na base")
            continue
        
        textos_resultado = []
        
        for resultado in resultados:
            texto = resultado[0].page_content
            textos_resultado.append(texto)
        
        base_conhecimento = "\n\n----\n\n".join(textos_resultado)
        
        response = chain.invoke({"base_conhecimento": base_conhecimento, "pergunta": pergunta})
        print(response.content)

perguntar()

        
    
