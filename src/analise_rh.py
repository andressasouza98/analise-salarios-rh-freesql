import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set(style="whitegrid")

# ==========================================================
# 1. CAMINHOS DOS ARQUIVOS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DADOS_DIR = BASE_DIR / "dados"
IMAGENS_DIR = BASE_DIR / "imagens"

IMAGENS_DIR.mkdir(exist_ok=True)

ARQ_Q1 = DADOS_DIR / "query_01.csv"
ARQ_Q2 = DADOS_DIR / "query_02.csv"

# ==========================================================
# 2. CARREGAMENTO DOS DADOS
# ==========================================================
df_q1 = pd.read_csv(ARQ_Q1)
df_q2 = pd.read_csv(ARQ_Q2)

# ==========================================================
# 3. CÓPIA DOS DADOS ORIGINAIS
# Preserva a base bruta para consulta e comparação
# ==========================================================
df_q1_raw = df_q1.copy()
df_q2_raw = df_q2.copy()

# ==========================================================
# 4. RENOMEAÇÃO DAS COLUNAS (MESMO PADRÃO DO NOTEBOOK)
# ==========================================================
df_q1 = df_q1_raw.rename(columns={
    "EMPLOYEE_ID": "id_funcionario",
    "FIRST_NAME": "nome",
    "LAST_NAME": "sobrenome",
    "SALARY": "salario",
    "DEPARTMENT_ID": "id_departamento",
    "DEPARTMENT_NAME": "nome_departamento",
    "JOB_ID": "id_cargo",
    "JOB_TITLE": "cargo",
    "MIN_SALARY": "salario_minimo_cargo",
    "MAX_SALARY": "salario_maximo_cargo"
})

df_q2 = df_q2_raw.rename(columns={
    "EMPLOYEE_ID": "id_funcionario",
    "FIRST_NAME": "nome",
    "LAST_NAME": "sobrenome",
    "SALARY": "salario",
    "DEPARTMENT_ID": "id_departamento",
    "DEPARTMENT_NAME": "nome_departamento",
    "LOCATION_ID": "id_local",
    "CITY": "cidade",
    "STATE_PROVINCE": "estado_provincia",
    "COUNTRY_ID": "id_pais",
    "COUNTRY_NAME": "pais",
    "REGION_ID": "id_regiao",
    "REGION_NAME": "regiao"
})

# ==========================================================
# 5. LIMPEZA DOS DADOS
# Remove qualquer linha com nulos e duplicatas
# ==========================================================
print("=" * 60)
print("LIMPEZA DOS DADOS")
print("=" * 60)

print(f"\nQuery 1 - linhas antes da limpeza: {df_q1.shape[0]}")
print(f"Query 2 - linhas antes da limpeza: {df_q2.shape[0]}")

df_q1 = df_q1.dropna().drop_duplicates()
df_q2 = df_q2.dropna().drop_duplicates()

print(f"\nQuery 1 - linhas após limpeza: {df_q1.shape[0]}")
print(f"Query 2 - linhas após limpeza: {df_q2.shape[0]}")

# ==========================================================
# 6. ESTATÍSTICAS DESCRITIVAS
# ==========================================================
print("\n" + "=" * 60)
print("ESTATÍSTICAS DESCRITIVAS")
print("=" * 60)

print("\nQuery 1 - Estatísticas salariais")
print("Média:", df_q1["salario"].mean())
print("Mediana:", df_q1["salario"].median())
print("Máximo:", df_q1["salario"].max())
print("Mínimo:", df_q1["salario"].min())
print("Desvio padrão:", df_q1["salario"].std())

print(df_q1["salario"].describe())

print("\nQuery 2 - Estatísticas salariais")
print("Média:", df_q2["salario"].mean())
print("Mediana:", df_q2["salario"].median())
print("Máximo:", df_q2["salario"].max())
print("Mínimo:", df_q2["salario"].min())
print("Desvio padrão:", df_q2["salario"].std())
print(df_q2["salario"].describe())

# ==========================================================
# 7. FREQUÊNCIA DAS CATEGORIAS (QUERY 2)
# ==========================================================
print("\n" + "=" * 60)
print("FREQUÊNCIA DAS CATEGORIAS - QUERY 2")
print("=" * 60)

print("\nDepartamentos:")
print(df_q2["nome_departamento"].value_counts())

print("\nRegiões:")
print(df_q2["regiao"].value_counts())

# ==========================================================
# 8. COMPARAÇÕES E MÉDIAS
# ==========================================================
print("\n" + "=" * 60)
print("COMPARAÇÕES SALARIAIS")
print("=" * 60)

print("\nMédia salarial por cargo (Query 1)")
media_cargo = df_q1.groupby("cargo")["salario"].mean().sort_values().round(2)
print(media_cargo)

print("\nMédia salarial por departamento (Query 2)")
media_dep = df_q2.groupby("nome_departamento")["salario"].mean().sort_values().round(2)
print(media_dep)

print("\nMédia salarial por região (Query 2)")
media_regiao = df_q2.groupby("regiao")["salario"].mean().sort_values().round(2)
print(media_regiao)

# ==========================================================
# 9. IDENTIFICAÇÃO DE OUTLIERS (QUERY 2)
# ==========================================================
q1 = df_q2["salario"].quantile(0.25)
q3 = df_q2["salario"].quantile(0.75)
iqr = q3 - q1

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = df_q2[
    (df_q2["salario"] < limite_inferior) |
    (df_q2["salario"] > limite_superior)
]

print("\n" + "=" * 60)
print("OUTLIERS SALARIAIS - QUERY 2")
print("=" * 60)
print(f"Q1: {q1:.2f}")
print(f"Q3: {q3:.2f}")
print(f"IQR: {iqr:.2f}")
print(f"Limite inferior: {limite_inferior:.2f}")
print(f"Limite superior: {limite_superior:.2f}")
print(f"Total de outliers: {outliers.shape[0]}")
print("\nExemplos de outliers:")
print(outliers[["nome", "sobrenome", "nome_departamento", "regiao", "salario"]].head())

# ==========================================================
# 10. GRÁFICOS (QUERY 2)
# ==========================================================

# Histograma - distribuição dos salários
plt.figure(figsize=(8, 4))
sns.histplot(df_q2["salario"], bins=20, kde=True)
plt.title("Distribuição dos salários")
plt.xlabel("Salário")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig(IMAGENS_DIR / "histograma_salarios_q2.png", dpi=300)
plt.close()

# Boxplot - salário por departamento
plt.figure(figsize=(10, 4))
sns.boxplot(data=df_q2, x="nome_departamento", y="salario")
plt.title("Distribuição dos salários por departamento")
plt.xlabel("Departamento")
plt.ylabel("Salário")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(IMAGENS_DIR / "boxplot_salarios_departamento_q2.png", dpi=300)
plt.close()

# Boxplot - salário por região
plt.figure(figsize=(8, 4))
sns.boxplot(data=df_q2, x="regiao", y="salario")
plt.title("Distribuição dos salários por região")
plt.xlabel("Região")
plt.ylabel("Salário")
plt.tight_layout()
plt.savefig(IMAGENS_DIR / "boxplot_salarios_regiao_q2.png", dpi=300)
plt.close()

# Barplot - média salarial por região
plt.figure(figsize=(8, 4))
sns.barplot(
    data=df_q2,
    x="regiao",
    y="salario",
    estimator="mean",
    errorbar=None
)
plt.title("Média salarial por região")
plt.xlabel("Região")
plt.ylabel("Salário médio")
plt.tight_layout()
plt.savefig(IMAGENS_DIR / "barplot_media_regiao_q2.png", dpi=300)
plt.close()

print("\nAnálise concluída com sucesso.")
print(f"Os gráficos foram salvos em: {IMAGENS_DIR}")