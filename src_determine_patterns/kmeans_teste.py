import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import glob

# Função para preparar dados para KMeans
def prepare_to_kmeans(cyclist):
    combined_df = pd.concat(cyclist, axis=1)
    dsk_means = np.concatenate([combined_df[feat].values.T for feat in ['Ck', 'Ca', 'Ke', 'Ge']], axis=1)
    return dsk_means

# Função para realizar a clusterização KMeans
def perform_kmeans(data, n_clusters=5, n_init=10, max_iter=500):
    kmeans = KMeans(n_clusters=n_clusters, n_init=n_init, max_iter=max_iter).fit(data)
    return kmeans

# Função para converter os centros dos clusters em DataFrames
def centers_to_dfs(centers, template_df):
    dfs = []
    for center in centers:
        df_temp = template_df.copy()
        df_temp[:] = np.nan
        for i, col in enumerate(['Ck', 'Ca', 'Ke', 'Ge']):
            df_temp[col] = center[:, i * len(template_df): (i + 1) * len(template_df)]
        dfs.append(df_temp)
    return dfs

# Função para salvar DataFrames em CSV
def save_dfs_to_csv(dfs, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i, df in enumerate(dfs, start=1):
        df.to_csv(os.path.join(folder_path, f'df_cl{i}.csv'))

# Carregar dados
ENERGETICSPATH = 'C:/Users/matheus/Desktop/danilo/energetic_patterns_cyclones_south_atlantic/csv_database_energy_by_periods/'
CSVSAVEPATH = 'C:/Users/matheus/Desktop/danilo/energetic_patterns_cyclones_south_atlantic/csv_patterns/'

all_files = []
files = glob.glob(os.path.join(ENERGETICSPATH, "*.csv"))
all_files.extend(files)

# Creating a list to save all dataframes
cyclist1= []

# Reading all files and saving in a list of dataframes
for case in all_files:
  columns_to_read = ['Ck','Ca', 'Ke', 'Ge']
  dfcyc = pd.read_csv(case,header=0,index_col=0)
  dfcyc = dfcyc[columns_to_read]
  cyclist1.append(dfcyc)

tipos_e_listas = {
    'tipo_1': {'fases': {'incipient', 'intensification', 'mature', 'decay'}, 'list': []},
    'tipo_2': {'fases': {'intensification', 'decay'}, 'list': []},
    'tipo_3': {'fases': {'intensification', 'mature', 'decay'}, 'list': []},
    'tipo_4': {'fases': {'incipient', 'intensification', 'mature', 'decay', 'residual'}, 'list': []},
    'tipo_5': {'fases': {'incipient', 'intensification', 'mature', 'decay', 'intensification 2', 'mature 2', 'decay 2'}, 'list': []},
}
def classificar_e_adicionar(df, tipos_e_listas):
    fases_presentes = set(df.index.dropna())
    for tipo, dados in tipos_e_listas.items():
        if fases_presentes == dados['fases']:
            dados['list'].append(df)
            return  


for df in cyclist1:
    classificar_e_adicionar(df, tipos_e_listas)


# Processamento principal

num_clusters = 5

for tipo, cyclists in tipos_e_listas.items():
    dsk_means = prepare_to_kmeans(cyclists)
    mk = perform_kmeans(dsk_means, num_clusters=num_clusters)
    centers = [mk.cluster_centers_[:, i * len(cyclists[0]):(i + 1) * len(cyclists[0])] for i in range(4)]
    dfs_clusters = centers_to_dfs(centers, cyclists[0])
    save_dfs_to_csv(dfs_clusters, os.path.join(CSVSAVEPATH, f'tipo_{tipo}'))

# Certifique-se de que a lógica de classificação esteja corretamente implementada para preencher cyclist_by_type
for file in files:
    df = pd.read_csv(file, header=0, index_col=0, usecols=['Ck', 'Ca', 'Ke', 'Ge'])
    classificar_e_adicionar(df)

