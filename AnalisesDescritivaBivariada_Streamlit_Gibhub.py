import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Análises Descritivas Profissional", layout="wide")

st.title("Análises Descritivas Profissional - Shell")


# Upload do arquivo
url = "https://raw.githubusercontent.com/Aran07Morales/AnalisesDescritivasShell/refs/heads/main/ArquivoDados.csv"

# Carregar o dataset
try:
        df = pd.read_csv(url, sep=';',encoding='utf-8')
        st.write("Dados carregados com sucesso:")
        st.dataframe(df)
except Exception as e:
        st.error(f"Erro ao carregar o Excel: {e}")


# Detectar tipos de variáveis
categorial_cols = df.select_dtypes(include=['object']).columns.tolist()
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

tipo_analise = st.radio("Escolha o tipo de análise:", ("Univariada", "Bivariada"))

if tipo_analise == "Univariada":
        tipo_var = st.radio("Tipo de variável:", ('Categórica', 'Numérica'))

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

elif tipo_analise == "Bivariada":
        st.subheader("Análise Bivariada")
        col_x = st.selectbox("Escolha a variável X:", df.columns, key="x")
        col_y = st.selectbox("Escolha a variável Y:", df.columns, key="y")

        if col_x and col_y:
            with st.expander("Tabela de Contingência (se aplicável)"):
                if df[col_x].dtype == 'object' and df[col_y].dtype == 'object':
                    crosstab = pd.crosstab(df[col_x], df[col_y])
                    st.dataframe(crosstab)

            with st.expander("Gráfico de Dispersão ou Barras"):
                fig, ax = plt.subplots(figsize=(10, 5))
                if df[col_x].dtype != 'object' and df[col_y].dtype != 'object':
                    sns.scatterplot(data=df, x=col_x, y=col_y, ax=ax)
                    plt.title(f'Dispersão: {col_x} vs {col_y}')
                elif df[col_x].dtype == 'object' and df[col_y].dtype != 'object':
                    sns.boxplot(x=col_x, y=col_y, data=df, ax=ax)
                    plt.title(f'Boxplot: {col_x} vs {col_y}')
                elif df[col_x].dtype != 'object' and df[col_y].dtype == 'object':
                    sns.boxplot(x=col_y, y=col_x, data=df, ax=ax)
                    plt.title(f'Boxplot: {col_y} vs {col_x}')
                else:
                    cross = pd.crosstab(df[col_x], df[col_y])
                    cross.plot(kind='bar', stacked=True, ax=ax)
                    plt.title(f'Cruzamento: {col_x} vs {col_y}')
                    plt.xlabel(col_x)
                    plt.ylabel("Contagem")
                    plt.xticks(rotation=45)
                st.pyplot(fig)