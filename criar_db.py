from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

# ver como trocar para a api do gemini

load_dotenv()

PASTA_base = "base"

def criar_db():
    #carregar documento
    #dividir os documentos em chuncks
    #vetorizar chuncks
    documentos = carregar_documentos()
    print(documentos)
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

def carregar_documentos():
    #vai ler se for pdf
    carregador = PyPDFDirectoryLoader(PASTA_base, glob="*.pdf")
    documentos = carregador.load()
    return documentos

def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap=400,
        length_function = len,
        add_start_index=True
    )
    chunks = separador_documentos.split_documents(documentos)
    print(len(chunks))
    return chunks

def vetorizar_chunks(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    db = Chroma.from_documents(chunks, embeddings, persist_directory="database")
    
    print("")
    print("Banco de Dados Criado") 
    print("")
    
if __name__ == "__main__":
    criar_db()