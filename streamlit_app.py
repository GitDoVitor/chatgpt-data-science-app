import streamlit as st
import pandas as pd
from openai import OpenAI

def send_message(message):    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "Você agora é um bot de análise de dados! Seu objetivo é ajudar o usuário a ter ideias de como analisar os dados do dataframe que ele carregou. Para isso você deve gerar insights ou ideias de análises para o usuário. Seu limite é de 5 insights."},
            {"role": "user", "content": f'{message}'}
        ]
    )
    
    return response.choices[0].message

st.set_page_config(page_title="Gerar Insights", page_icon="👀", layout="wide", initial_sidebar_state="collapsed")


#### SIDE BAR ####
with st.sidebar:  
    st.markdown("###### Desenvolvido por [João Vitor](https://github.com/GitDoVitor)")


#### MAIN PAGE ####
st.title("Gere Insights ou ideias para análises com apenas um clique! 👀")
st.write("A ideia é facilitar a vida de quem precisa de insights para análises de dados, mas não tem ideia de onde começar. Para isso, basta fazer o upload de um arquivo .csv contendo os dados que você deseja analisar e pronto! O sistema irá gerar uma série de dicas para te ajudar a ter ideias de como analisar os dados. 😁")

st.divider()

csv = st.file_uploader("Faça o upload do seu arquivo .csv aqui:", type=["csv"])

if not csv:
    st.warning("Por favor, faça o upload do seu arquivo .csv para continuar.")
elif csv:
    st.success("Arquivo .csv carregado com sucesso! 🎉")
    
    OPENAI_API_KEY= st.text_input("Digite sua API Key do OpenAI aqui:")

    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    col1, col2 = st.columns(2)
    with col1:
        df_divider = st.selectbox("Qual o tipo de separador utilizado no seu arquivo?", [",", ";"])
    with col2:
        df_encoding = st.selectbox("Qual o tipo de encoding utilizado no seu arquivo?", ["utf-8", "latin-1", "ISO-8859-9", "Outro"])
        if df_encoding == "Outro":
            df_encoding = st.text_input("Digite o tipo de encoding utilizado no seu arquivo: Ex: utf-8, latin-1, ISO-8859-9, etc.")
    
st.divider()

if csv:
    df = pd.read_csv(csv, sep=df_divider, encoding=df_encoding)
    st.write("#### Abaixo, você pode conferir uma prévia dos seus dados:")
    st.dataframe(df.head(5))

    gerar_insights = st.button("Gerar Insights 🚀")
    
    if gerar_insights:
        st.divider()
        response = send_message(df.head(5))
        st.write(response.content)