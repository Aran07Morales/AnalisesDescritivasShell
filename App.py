import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cache para acelerar o carregamento dos dados
### @st.cache_data
       
def main():
    df = None;
    ### url = "https://drive.google.com/uc?id=1Vi30VtLuXA6QczPFUZZqkXMwFDE9_VO5"
    ### url = "https://drive.google.com/uc?id=17CGFrn_iVcUhwmNF5d581MqY2vooi-1k"
    ### url = "https://drive.google.com/uc?id=1g205E43Go7f_X47zCvtMXx3Ag1GF25rO"
    
    url = "https://raw.githubusercontent.com/Aran07Morales/AnalisesDescritivasShell/refs/heads/main/TRATADO_Filtrado_teste.csv"
   
    st.title("App de Análise Descritiva")
    st.markdown("""
    Este aplicativo carrega um arquivo CSV e realiza:
    - Análise univariada
    - Análise bivariada (categórica vs categórica)
    - Matriz de correlação
    - Detecção de valores faltantes
    - Detecção de outliers (IQR)
    """)

    # 1. Entrada da URL
    
    try:
        ### df = pd.read_excel(url)
        df = pd.read_csv(url, sep=';',encoding='utf-8')
        st.write("Dados carregados com sucesso:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Erro ao carregar o Excel: {e}")
    
   
    # 2. Carregamento dos dados    
    #if url:
    #    try:
    #      df = load_data_from_url(url)
    #      st.success("Arquivo carregado com sucesso!")
    #      st.dataframe(df.head())
        # Aqui você chama as outras análises se quiser
    #    except Exception as e:
    #      st.error("Erro ao carregar o arquivo. Verifique se a URL é válida e pública.")
    #      st.exception(e)
    #else:
    #    st.info("Por favor, informe uma URL pública para o CSV.")

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
            ax.hist(df[col].dropna(), bins=30, edgecolor='black')
            ax.set_title(f'Distribuição de {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequência')
            st.pyplot(fig)

        # 3. Análise Bivariada
    st.header("3. Análise Bivariada")
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if len(cat_cols) >= 2:
            x = st.selectbox("Selecione a variável categórica X", cat_cols)
            y = st.selectbox("Selecione a variável categórica Y", cat_cols, index=1)
            ct = pd.crosstab(df[x], df[y], normalize='index')
            st.subheader(f'Cruzamento {x} vs {y} (proporção)')
            st.dataframe(ct)
            fig, ax = plt.subplots()
            ct.plot(kind='bar', stacked=True, ax=ax)
            ax.set_ylabel('Proporção')
            ax.set_xlabel(x)
            plt.tight_layout()
            st.pyplot(fig)

        # 4. Matriz de Correlação
    st.header("4. Matriz de Correlação")
    corr = df[numeric_cols].corr()
    st.dataframe(corr)
    fig, ax = plt.subplots()
    cax = ax.imshow(corr.values, interpolation='nearest', cmap='coolwarm')
    fig.colorbar(cax)
    ax.set_xticks(range(len(numeric_cols)))
    ax.set_xticklabels(numeric_cols, rotation=45)
    ax.set_yticks(range(len(numeric_cols)))
    ax.set_yticklabels(numeric_cols)
    for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha='center', va='center', color='black')
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

