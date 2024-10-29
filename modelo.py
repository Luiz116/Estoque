import pandas as pd
import numpy as np
import sys
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

# Carregar os datasets
entradas_path = sys.argv[1]
produtos_path = sys.argv[2]
saidas_path = sys.argv[3]

entradas = pd.read_csv(entradas_path, header=None, delimiter=';')
produtos = pd.read_csv(produtos_path, header=None, delimiter=';')
saidas = pd.read_csv(saidas_path, header=None, delimiter=';')

# Nomeando as colunas
entradas.columns = ['Produto_ID', 'Quantidade_Entrada', 'Data_Entrada', 'Quantidade_Atual', 'Preco_Total_entrada']
saidas.columns = ['Produto_ID', 'Quantidade_Saida', 'Data_Saida', 'Quantidade_Atual', 'Preco_Total_saida']
produtos.columns = ['Produto_ID', 'Descricao_Produto']

# Removendo padrão de horas das datas
entradas['Data_Entrada'] = entradas['Data_Entrada'].str.replace(r'\s00:00:00\.000', '', regex=True)
saidas['Data_Saida'] = saidas['Data_Saida'].str.replace(r'\s00:00:00\.000', '', regex=True)

# Lidando com valores nulos e outliers
entradas.fillna(0, inplace=True)
saidas.fillna(0, inplace=True)
entradas = entradas[(np.abs(entradas['Quantidade_Entrada'] - entradas['Quantidade_Entrada'].mean()) <= (3 * entradas['Quantidade_Entrada'].std()))]
saidas = saidas[(np.abs(saidas['Quantidade_Saida'] - saidas['Quantidade_Saida'].mean()) <= (3 * saidas['Quantidade_Saida'].std()))]

# Renomear para evitar conflitos e unir os dados
entradas.rename(columns={'Data_Entrada': 'Data'}, inplace=True)
saidas.rename(columns={'Data_Saida': 'Data'}, inplace=True)
dados_completos = pd.merge(entradas, produtos, on='Produto_ID', how='outer', suffixes=('_entrada', '_produto'))
dados_completos = pd.merge(dados_completos, saidas, on=['Produto_ID', 'Data'], how='outer')

# Feature Engineering Avançado
dados_completos['Data'] = pd.to_datetime(dados_completos['Data'], errors='coerce')
dados_completos['Ano'] = dados_completos['Data'].dt.year
dados_completos['Mes'] = dados_completos['Data'].dt.month
dados_completos['Dia'] = dados_completos['Data'].dt.day
dados_completos['Dia_da_Semana'] = dados_completos['Data'].dt.weekday
dados_completos.fillna(0, inplace=True)

# Definindo X e y para o modelo
X = dados_completos[['Quantidade_Entrada', 'Preco_Total_entrada', 'Preco_Total_saida', 'Ano', 'Mes', 'Dia', 'Dia_da_Semana']]
y = dados_completos['Quantidade_Saida']

# Pipeline para Modelo com Validação Cruzada
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestRegressor(random_state=42))
])

# Definindo a busca de hiperparâmetros
param_grid = {
    'model__n_estimators': [50, 100, 200],
    'model__max_depth': [None, 10, 20, 30],
    'model__min_samples_split': [2, 5, 10],
    'model__min_samples_leaf': [1, 2, 4],
}

random_search = RandomizedSearchCV(pipeline, param_grid, n_iter=10, cv=5, random_state=42, n_jobs=-1)
random_search.fit(X, y)

# Avaliação do modelo com cross-validation
scores = cross_val_score(random_search.best_estimator_, X, y, cv=5, scoring='neg_mean_squared_error')
rmse_scores = np.sqrt(-scores)

# Avaliação do modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
best_model = random_search.best_estimator_
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

# Avaliação Final
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Gráfico de Previsões vs Valores Reais
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Valores Reais")
plt.ylabel("Previsões")
plt.title("Previsões vs Valores Reais")
plt.savefig('previsoes_vs_reais.png')
plt.close()

# Modelo treinado
joblib.dump(best_model, 'modelo_previsao_estoque.pkl')

# Printar os resultados
with open('resultados.txt', 'w') as f:
    f.write("Melhores Hiperparâmetros: {}\n".format(random_search.best_params_))
    f.write("RMSE médio (Cross-Validation): {}\n".format(rmse_scores.mean()))
    f.write("\nAvaliação do Modelo Refinado:\n")
    f.write("MAE: {}\n".format(mae))
    f.write("MSE: {}\n".format(mse))
    f.write("RMSE: {}\n".format(rmse))
    f.write("R² Score: {}\n".format(r2))
