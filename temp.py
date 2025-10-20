import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("Controle de Produção")
aba1, aba2, aba3 = st.tabs(["📁 Arquivo CSV", "➕ Novo Registro", "📊 Análises"])


with aba1:
    st.subheader("Carregar ou Salvar Arquivo CSV")

    arquivo = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

    if arquivo is not None:
        df = pd.read_csv(arquivo)
        st.success("Arquivo carregado com sucesso!")
        df.to_csv("dados_temp.csv", index=False)  # Salva o conteúdo carregado
    else:
        if os.path.exists("dados_temp.csv"):
            df = pd.read_csv("dados_temp.csv")
        else:
            df = pd.DataFrame(columns=["Data", "Máquina", "Turno", "Peças Totais", "Peças Defeituosas"])

    st.dataframe(df)

    nome = st.text_input("Nome do novo arquivo CSV", "dados_atualizados.csv")
    if st.button("Salvar arquivo"):
        df.to_csv(nome, index=False)
        st.success(f"Arquivo salvo como: {nome}")


with aba2:
    st.subheader("Adicionar novo registro de produção")

    data = st.text_input("Data (ex: 2025-10-18)")
    maquina = st.text_input("Máquina")
    turno = st.text_input("Turno (ex: Manhã, Tarde, Noite)")
    pecas_totais = st.number_input("Peças Totais", min_value=0)
    pecas_defeituosas = st.number_input("Peças Defeituosas", min_value=0)

    if st.button("Adicionar registro"):
        novo = pd.DataFrame({
            "Data": [data],
            "Máquina": [maquina],
            "Turno": [turno],
            "Peças Totais": [pecas_totais],
            "Peças Defeituosas": [pecas_defeituosas]
        })

        if os.path.exists("dados_temp.csv"):
            df = pd.read_csv("dados_temp.csv")
            df = pd.concat([df, novo], ignore_index=True)
        else:
            df = novo

        df.to_csv("dados_temp.csv", index=False)
        st.success("Registro adicionado e salvo em 'dados_temp.csv'!")
        st.dataframe(df)


with aba3:
    st.subheader("Análises e Indicadores de Produção")

    if os.path.exists("dados_temp.csv"):
        df = pd.read_csv("dados_temp.csv")
    else:
        st.info("Nenhum dado disponível. Adicione ou carregue um arquivo primeiro.")
        df = pd.DataFrame()

    if len(df) > 0:
        df["Eficiência (%)"] = ((df["Peças Totais"] - df["Peças Defeituosas"]) /
                                df["Peças Totais"].replace(0, 1)) * 100

        st.write("Tabela de dados com eficiência calculada:")
        st.dataframe(df)
        alerta = df[(df["Eficiência (%)"] < 90) | (df["Peças Totais"] < 80)]
        if len(alerta) > 0:
            st.warning("⚠️ Registros com baixa eficiência (<90%) ou baixa produção (<80 peças):")
            st.dataframe(alerta)
        st.subheader("Produção por Máquina")
        fig1, ax1 = plt.subplots()
        ax1.bar(df["Máquina"], df["Peças Totais"], color="steelblue")
        ax1.set_xlabel("Máquina")
        ax1.set_ylabel("Peças Totais")
        ax1.set_title("Produção por Máquina")
        st.pyplot(fig1)
        st.subheader("Eficiência por Máquina")
        fig2, ax2 = plt.subplots()
        ax2.plot(df["Máquina"], df["Eficiência (%)"], marker='o', color="orange")
        ax2.set_xlabel("Máquina")
        ax2.set_ylabel("Eficiência (%)")
        ax2.set_title("Eficiência por Máquina")
        st.pyplot(fig2)
        media = df["Eficiência (%)"].mean().round(2)
        st.write("Eficiência Média Geral (%)", media)
    else:
        st.info("Nenhum dado para mostrar. Adicione registros primeiro.")