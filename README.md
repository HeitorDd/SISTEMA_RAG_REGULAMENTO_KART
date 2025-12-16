🏎️ Assistente de Regulamento de Kart (RAG)
Este projeto é um assistente inteligente baseado em RAG (Retrieval-Augmented Generation) que permite aos usuários tirar dúvidas sobre regulamentos de competições de Kart. O sistema lê arquivos PDF, processa as informações e utiliza o Google Gemini para responder perguntas com fundamentação técnica e citações dos artigos.

📋 Funcionalidades
• Consulta Técnica: Responde dúvidas sobre regras, punições e especificações técnicas.
• Fundamentação: Cita exatamente o artigo do regulamento utilizado na resposta.
• Interface Web: Interface amigável construída com Streamlit.
• Modo CLI: Opção de uso via terminal.
• Atualização Dinâmica: Recriação do banco de dados vetorial quando novos PDFs são adicionados.

🛠️ Tecnologias Utilizadas
• Python
• LangChain
• Google Gemini (Generative AI)
• ChromaDB (Vector Store)
• Streamlit

📂 Estrutura do Projeto
SISTEMA_RAG_KART/
│
├── base/             # Coloque os PDFs do regulamento aqui
├── database/         # Onde o banco de dados vetorial (Chroma) será salvo
├── .env              # Arquivo de variáveis de ambiente (API Key)
├── app.py            # Aplicação Web (Streamlit)
├── criar_db.py       # Script para criar/atualizar o banco de dados
├── main.py           # Versão CLI (Chat no terminal)
└── requirements.txt  # Dependências do projeto


🚀 Como Rodar o Projeto
Siga os passos abaixo para configurar o ambiente e executar o assistente.
1. Pré-requisitos
Certifique-se de ter uma API Key do Google Gemini. Você pode obtê-la no Google AI Studio.
2. Configuração do Ambiente
Clone o repositório:
git clone [https://github.com/SEU-USUARIO/NOME-DO-REPO.git](https://github.com/HeitorDd/SISTEMA_RAG_REGULAMENTO_KART.git)
cd SISTEMA_RAG_KART


Crie e ative o ambiente virtual (.venv):
Windows:
python -m venv .venv
.\.venv\Scripts\activate


Linux/Mac:
python3 -m venv .venv
source .venv/bin/activate


Instale as dependências:
pip install -r requirements.txt


Configure a API Key:
Crie um arquivo chamado .env na raiz do projeto.
Adicione a seguinte linha dentro dele:
GOOGLE_API_KEY="Sua_Chave_Aqui"


3. Criando o Banco de Dados
Antes de rodar a aplicação, é necessário processar os PDFs.
Coloque seus arquivos PDF na pasta base.
Execute o script de criação do banco:
python criar_db.py

Isso criará a pasta database com os vetores.
4. Executando a Aplicação
Agora você pode iniciar a interface web:
streamlit run app.py


O navegador abrirá automaticamente no endereço local (geralmente http://localhost:8501).
Nota: Se preferir usar pelo terminal sem interface gráfica, você pode rodar:
python main.py
