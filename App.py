import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cache para acelerar o carregamento dos dados
#@st.cache
@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file, sep=';')
    
    
    ## df = pd.read_excel('caminho/para/arquivo.xls', engine='xlrd')

def main():
    st.title("App de Análise Descritiva")
    st.markdown("""
    Este aplicativo carrega um arquivo CSV e realiza:
    - Análise univariada
    - Análise bivariada (categórica vs categórica)
    - Matriz de correlação
    - Detecção de valores faltantes
    - Detecção de outliers (IQR)
    """
    )

    uploaded_file = st.file_uploader("TRATADO_Filtrado_teste.csv", type="csv")
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # 1. Visualização inicial
        st.header("1. Visualização dos Dados")
        st.dataframe(df.head())

        # 2. Análise Univariada
        st.header("2. Estatísticas Descritivas Univariadas")
        desc = df.describe(include='all').T
        st.dataframe(desc)

        # Histogramas
        st.subheader("Histogramas")
        numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
        for col in numeric_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(f'Distribuição de {col}')
            st.pyplot(fig)

        # 3. Análise Bivariada
        st.header("3. Análise Bivariada")
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        if len(cat_cols) >= 2:
            x = st.selectbox("Variável Categórica X", cat_cols)
            y = st.selectbox("Variável Categórica Y", cat_cols, index=1)
            if x and y:
                ct = pd.crosstab(df[x], df[y], normalize='index')
                st.subheader(f'Cruzamento {x} vs {y} (proporção)')
                st.dataframe(ct)
                fig, ax = plt.subplots()
                ct.plot(kind='bar', stacked=True, ax=ax)
                ax.set_ylabel('Proporção')
                st.pyplot(fig)

        # 4. Correlação
        st.header("4. Matriz de Correlação")
        corr = df[numeric_cols].corr()
        st.dataframe(corr)
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)

        # 5. Valores Faltantes
        st.header("5. Valores Faltantes")
        missing = df.isnull().sum().to_frame('missing_count')
        st.dataframe(missing)

        # 6. Detecção de Outliers (IQR)
        st.header("6. Outliers (Método IQR)")
        outliers = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            mask = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
            outliers[col] = int(mask.sum())
        outliers_df = pd.DataFrame.from_dict(outliers, orient='index', columns=['outliers_count'])
        st.dataframe(outliers_df)

if __name__ == "__main__":
    main()
