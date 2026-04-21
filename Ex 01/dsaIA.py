# Importar biblioteca os para interagir com o sistema operacional
import os

# Importar biblioteca streamlit para criar a interface web criativa
import streamlit as st

# Importar a classe Groq para se conectar à API da plataforma e poder usar o modelo LLM
from groq import Groq

# Configura a pagina inicial do Streamlit com titulo, icon, layout e estado da barra lateral
st.set_page_config(
    page_title="DSA AI Assitent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """
Você é o "DSA Coder", um assistente de IA especialista em programação, com foco principal em Python. Sua missão é ajudar desenvolvedores com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Configurando e customizando a sidebar
with st.sidebar:

    # Definição do Titulo da sidebar
    st.title("🤖 DSA AI Assistant")

    # Uma breve explicação sobre o site 
    st.markdown("Um assistente de IA focado em programação Python para ajudar iniciantes")

    # caixa para colocar a API key do usuario
    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    # Linha para separar conteudo
    st.markdown("---")
    st.markdown("Desenvolvido com objetivo de ajudar nas dúvidas de programação com Python. A IA pode cometer erros. " \
    "Verifique as respostas")

# Titulos da pagina principal
st.title("DSA AI Assistant - By Thayay")
st.title("Assistente Pessoal de Programação em Python 🐍")

st.caption("Faça sua pergunta sobre a Linguagem Python e obtenha codigo, explicações e referências.")

# Inicializa o histórico de mensagens da sessão, caso não tenha sido inicializado ainda
if "messages" not in st.session_state:
    st.session_state.messages = []

# Esse for exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variavel do cliente Groq como none
client = None

# Se tiver colocado sua chave api ele entra no if
if groq_api_key:

    try:
        # Cria cliente Groq com a chave API fornecida
        client = Groq(api_key = groq_api_key)

    except Exception as e:
        # Exibe erro caso haja problema em inicializar a variavel
        st.sidebar.error(f"Erro ao inicializar cliente Groq : {e}")
        st.stop() # Para a aplicação

# Caso não tenha inserido a chave API mostra a mensagem
elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key do Groq na barra lateral para continuarmos")

# Captura a entrada do usuario, ou seja, sua pergunta
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):

    # Se o cliente não for válido, mostra um aviso e para a sessão
    if not client:
        st.warning("Por favor, insira sua API Key do Groq na barra lateral para continuarmos")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Exibe a mensagem do usuario no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Armazena o CUSTOM_PROMPT na variavel messages_for_api 
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]

    # Para cada mensagem no estado de mensagem, ela + o CUSTOM_PROMPT são enviados para a LLM pela API
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):

            try:
                # Chama a API do Groq para gerar a resposta da IA
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-120b",
                    temperature=1,
                    max_completion_tokens=2048
                )

                # Extrai a resposta gerada pela API e armazena na dsa_ai_resposta
                dsa_ai_resposta = chat_completion.choices[0].message.content

                # Mostra a resposta do assistente
                st.markdown(dsa_ai_resposta)

                # Armazena a resposta no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API do Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p> DSA AI Assistent - Parte Integrante do Curso de Fundamentos de Linguagem Python para IA da Data Science Academy</p>
    </div>
    """,
    unsafe_allow_html=True
)
