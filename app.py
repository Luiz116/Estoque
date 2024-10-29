import joblib
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

# Carregar o modelo
model = joblib.load('ml/modelo_previsao_estoque.pkl')

st.title("Previsão de Saída e Esgotamento de Estoque")

# Entrada de dados
produto_id = st.number_input("ID do Produto", min_value=1, step=1)
quantidade_entrada = st.number_input("Quantidade Entrada", min_value=0.0)
preco_total_entrada = st.number_input("Preço Total Entrada", min_value=0.0)
preco_total_saida = st.number_input("Preço Total Saída", min_value=0.0)
ano = st.number_input("Ano", min_value=2020, max_value=2030, value=datetime.now().year)
mes = st.number_input("Mês", min_value=1, max_value=12, value=datetime.now().month)
dia = st.number_input("Dia", min_value=1, max_value=31, value=datetime.now().day)
dia_da_semana = datetime(ano, mes, dia).weekday()

# Realizar a previsão de saída
if st.button("Prever Quantidade de Saída"):
    entrada = [[quantidade_entrada, preco_total_entrada, preco_total_saida, ano, mes, dia, dia_da_semana]]
    
    # Fazer a previsão
    quantidade_saida_prevista = model.predict(entrada)[0]
    st.write(f"Quantidade Prevista de Saída: {quantidade_saida_prevista:.2f} unidades")

    # Entrada da quantidade atual em estoque
    #quantidade_atual = st.number_input("Quantidade Atual em Estoque", min_value=0.0)
    
    # Previsão de esgotamento do estoque
    #if quantidade_saida_prevista > 0:
    #    dias_para_esgotamento = quantidade_atual / quantidade_saida_prevista
    #    data_esgotamento = datetime.now() + timedelta(days=dias_para_esgotamento)
    #    st.write(f"Data Estimada para Esgotamento do Estoque: {data_esgotamento.date()}")
    #else:
    #    st.write("Não foi possível estimar a data de esgotamento.")
