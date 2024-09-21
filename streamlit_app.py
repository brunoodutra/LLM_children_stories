import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from gradio_client import Client
import os


# Inicialização do modelo LLM
model_id = "llama3-8b-8192"
llm1 = ChatGroq(
    model=model_id, temperature=0.7, max_tokens=1023, timeout=None, max_retries=2,
)

# Inicialização do Gradio Client para Text-to-Speech
voice_Literal = ['', 'pt-BR-ThalitaNeural - pt-BR (Female)', 'pt-BR-AntonioNeural - pt-BR (Male)', 'pt-BR-FranciscaNeural - pt-BR (Female)']
client = Client("innoai/Edge-TTS-Text-to-Speech")

# Configuração da interface Streamlit
st.title("Gerador de Histórias Infantis")

def main():
    # Entrada inicial para o tema
    tema = st.text_input("Digite um tema para a história:")

    # Botão de resetar, que aparece após a introdução do tema
    if tema:
        reset_button = st.button("Resetar")
    else:
        reset_button = None

    # Verificação se os títulos já foram gerados
    if "titulos" not in st.session_state:
        st.session_state.titulos = []

    # Gera títulos se o tema foi inserido e os títulos ainda não foram gerados
    if tema and not st.session_state.titulos:
        prompt_template_titulos = PromptTemplate(
            input_variables=["tema"],
            template=(
                "Me ajude a listar somente 10 sugestões de títulos de história com o tema {tema}, "
                "sem nenhuma descrição, e não inclua nenhum texto extra. "
                "Somente os títulos separados por linha e em português."
            )
        )

        # Geração dos títulos
        chain_titulos = LLMChain(llm=llm1, prompt=prompt_template_titulos)
        st.session_state.titulos = chain_titulos.run(tema).split("\n")

    # Exibir as sugestões de títulos
    if st.session_state.titulos:
        st.subheader("Sugestões de Títulos:")
        titulo_escolhido = st.selectbox("Escolha um título:", st.session_state.titulos)

        # Botão para gerar a história
        if st.button("Gerar História"):
            if titulo_escolhido:
                # Template para gerar a história baseada no título escolhido
                prompt_template_historia = ChatPromptTemplate.from_messages([
                    ("system", "Você é um contator de Histórias, que tem o objetivo de elaborar uma história infantil de acordo com o Título fornecido. Elabore somente a história com no máximo 500 palavras, mantendo a coesão, criatividade e conclusão."), 
                    ("human", "{input}"),
                ])

                # Geração da história
                chain_historia = LLMChain(llm=llm1, prompt=prompt_template_historia)
                historia = chain_historia.run(titulo_escolhido)

                # Salvar a história no estado da sessão
                st.session_state.historia = historia

    # Conjunto de seleção de voz, botão e player de áudio
    if "historia" in st.session_state:
        # Seleção da voz
        voice_selection = st.selectbox("Escolha a voz:", voice_Literal[1:], key="voice_selection")

        # Botão para gerar o áudio
        if st.button("Gerar Áudio"):
            loading = st.empty()
            loading.text("Carregando...")  # Indica que está carregando
            selected_voice = voice_Literal[1:].index(voice_selection) + 1

            # Geração do áudio usando a API do Gradio Client
            result = client.predict(
                text=st.session_state.historia,
                voice=voice_Literal[selected_voice],
                rate=0,
                pitch=0,
                api_name="/predict"
            )

            # Armazenar a URL do áudio gerado no estado da sessão
            if result[0] is not None:
                st.session_state.audio_url = result[0]

            loading.empty()  # Remove o texto de carregando após a geração do áudio

        # Exibir e reproduzir o áudio
        if "audio_url" in st.session_state:
            st.subheader("Reproduzir o Áudio:")
            st.audio(st.session_state.audio_url, format="audio/mp3")

        # Exibir a história
        st.subheader("História Gerada:")
        st.write(st.session_state.historia)

    # Resetar a aplicação
    if reset_button:
        st.session_state.clear()  # Limpa todo o estado da sessão
        st.session_state.titulos = []  # Limpa títulos específicos
        st.session_state.historia = ""  # Limpa a história
        st.session_state.audio_url = ""  # Limpa a URL do áudio
        st.text_input("Digite um tema para a história:", value="", key="reset_tema")  # Limpa o campo de texto do tema
        st.write("A aplicação foi resetada. Por favor, insira um novo tema.")  # Mensagem opcional

if __name__ == "__main__":
    main()
