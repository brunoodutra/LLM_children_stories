import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Inicialização do modelo LLM
llm1 = OllamaLLM(model="llama3.1", temperature=0.7, max_new_tokens=512, max_length=512)

# Configuração da interface Streamlit
st.title("Gerador de Histórias Infantis")

# Entrada inicial para o tema
tema = st.text_input("Digite um tema para a história:")

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
            "Somente os títulos separados por linha."
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
            prompt_template_historia = PromptTemplate(
                input_variables=["titulo"],
                template=(
                    "Você escolheu o título '{titulo}'. Agora, elabore uma história infantil apropriada "
                    "para crianças de 3 a 5 anos."
                )
            )
            
            # Geração da história
            chain_historia = LLMChain(llm=llm1, prompt=prompt_template_historia)
            historia = chain_historia.run(titulo_escolhido)
            
            # Exibir a história gerada
            st.subheader("História Gerada:")
            st.write(historia)
