import pandas as pd
import io

try:
    import streamlit as st
except ModuleNotFoundError:
    print("Erro: A biblioteca 'streamlit' não está instalada. Certifique-se de rodar o código em um ambiente com 'streamlit' disponível.")
    exit()

# Função para processar o arquivo CSV
def processar_planilha(uploaded_file):
    if uploaded_file is not None:
        try:
            # Lendo o arquivo CSV
            df = pd.read_csv(uploaded_file)
            
            # Definindo as colunas a serem mantidas
            colunas_mantidas = [
                'Nome da Conta Financeira', 'Conciliado', 'Observação/Descrição', 'Competência',
                'Vencimento', 'Data Conciliação', 'Valor (R$)', 'Valor Realizado', 'Categoria', 'Cliente/Fornecedor'
            ]
            
            # Verificando se todas as colunas existem na planilha
            colunas_existentes = [col for col in colunas_mantidas if col in df.columns]
            
            if not colunas_existentes:
                st.error("O arquivo carregado não contém as colunas esperadas. Verifique e tente novamente.")
                return None
            
            # Criando um novo DataFrame apenas com as colunas desejadas
            df_filtrado = df[colunas_existentes]
            
            return df_filtrado
        except Exception as e:
            st.error(f"Erro ao processar o arquivo. Certifique-se de que é um arquivo CSV válido: {e}")
            return None
    return None

# Interface do app
st.set_page_config(page_title="Preparar Planilha Financeira", layout="wide")
st.title("📊 Preparar Planilha Financeira")
st.write("Carregue um arquivo CSV para processar e baixar uma versão otimizada com colunas essenciais.")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Escolha um arquivo CSV", type=["csv"], help="Envie um arquivo CSV para processar.")

if uploaded_file is not None:
    df_filtrado = processar_planilha(uploaded_file)
    
    if df_filtrado is not None:
        st.subheader("🔍 Pré-visualização dos dados filtrados")
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Criar arquivo CSV para download
        output = io.StringIO()
        df_filtrado.to_csv(output, index=False)
        processed_data = output.getvalue()
        
        # Disponibilizando para download
        st.download_button(
            label="⬇️ Baixar Planilha Processada",
            data=processed_data,
            file_name="planilha_processada.csv",
            mime="text/csv"
        )
