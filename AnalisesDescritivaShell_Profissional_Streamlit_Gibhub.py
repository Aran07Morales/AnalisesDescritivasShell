
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análises Descritivas ", layout="wide")

st.title("Análises Descritivas - Shell")

# Upload do arquivo
url = "https://raw.githubusercontent.com/Aran07Morales/AnalisesDescritivasShell/refs/heads/main/ArquivoDados.csv"

# Carregar o dataset
try:
        df = pd.read_csv(url, sep=';',encoding='utf-8')
        st.write("Dados carregados com sucesso:")
        st.dataframe(df)
except Exception as e:
        st.error(f"Erro ao carregar o Excel: {e}")
    
st.subheader("Prévia dos Dados")
st.dataframe(df.head())

# Detectar tipos de variáveis
categorial_cols = df.select_dtypes(include=['object']).columns.tolist()
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Escolher tipo de variável
tipo_var = st.radio("Qual tipo de variável você deseja analisar?", ('Categórica', 'Numérica'))

if tipo_var == 'Categórica':
        col_selecionada = st.selectbox("Escolha a variável categórica:", categorial_cols)
        if col_selecionada:
            freq = df[col_selecionada].value_counts(dropna=False)
            
            with st.expander("Tabela de Frequência"):
                st.dataframe(freq.to_frame(name='Frequência'))

            with st.expander("Gráfico de Distribuição"):
                fig, ax = plt.subplots(figsize=(10, 5))
                freq.plot(kind='bar', ax=ax)
                plt.title(f'Distribuição de: {col_selecionada}')
                plt.xlabel(col_selecionada)
                plt.ylabel('Contagem')
                plt.xticks(rotation=90)
                plt.tight_layout()
                st.pyplot(fig)

elif tipo_var == 'Numérica':
        col_selecionada = st.selectbox("Escolha a variável numérica:", numeric_cols)
        if col_selecionada:
            stats = df[col_selecionada].describe()
            
            with st.expander("Estatísticas Descritivas"):
                st.write(f"**Média:** {stats['mean']:.2f}")
                st.write(f"**Mediana:** {df[col_selecionada].median():.2f}")
                st.write(f"**Desvio Padrão:** {stats['std']:.2f}")
                st.write(f"**Mínimo:** {stats['min']:.2f}")
                st.write(f"**Máximo:** {stats['max']:.2f}")

            with st.expander("Histograma"):
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.hist(df[col_selecionada].dropna(), bins=30, edgecolor='black')
                plt.title(f'Distribuição: {col_selecionada}')
                plt.xlabel(col_selecionada)
                plt.ylabel('Frequência')
                st.pyplot(fig)
