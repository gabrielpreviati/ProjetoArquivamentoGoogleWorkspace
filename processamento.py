import pandas as pd
import unicodedata

# 1. Carregar os arquivos
try:
    df_google = pd.read_csv('users_google.csv')
    df_ativos = pd.read_csv('lista_ativos.csv')
except UnicodeDecodeError:
    df_google = pd.read_csv('users_google.csv', encoding='latin1')
    df_ativos = pd.read_csv('lista_ativos.csv', encoding='latin1')

# 2. Identificar coluna de nomes na lista de ativos
col_nome_ativos = df_ativos.columns[1]

# 3. Filtrar Domínio @emece.com.br
df_google_emece = df_google[
    df_google['Email Address [Required]'].str.endswith('@emece.com.br', na=False)
].copy()

# REMOVENDO ACENTOS E ESPAÇOS

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto = texto.lower()
    return " ".join(texto.split())

def extrair_primeiro_ultimo(nome_completo):
    nome_limpo = normalizar_texto(nome_completo)
    partes = nome_limpo.split()    
    if len(partes) == 0:
        return ""
    if len(partes) == 1:
        return partes[0]
    return f"{partes[0]} {partes[-1]}"

# 4. Processar nomes do Google
df_google_emece['NOME_COMPLETO_RAW'] = (
    df_google_emece['First Name [Required]'].fillna('') + ' ' + 
    df_google_emece['Last Name [Required]'].fillna('')
)

df_google_emece['KEY_MATCH'] = df_google_emece['NOME_COMPLETO_RAW'].apply(extrair_primeiro_ultimo)

df_ativos['KEY_MATCH'] = df_ativos[col_nome_ativos].apply(extrair_primeiro_ultimo)

keys_ativos_set = set(df_ativos['KEY_MATCH'].unique())

df_arquivar = df_google_emece[~df_google_emece['KEY_MATCH'].isin(keys_ativos_set)].copy()

coluna_login = next((col for col in df_google.columns if 'Last Sign In' in col), None)
if coluna_login:
    df_arquivar['ULTIMO_LOGIN'] = df_arquivar[coluna_login]
else:
    df_arquivar['ULTIMO_LOGIN'] = 'Info não encontrada'

df_final = pd.DataFrame()
df_final['Email Address'] = df_arquivar['Email Address [Required]']
df_final['New Status'] = 'Suspended'
df_final['NOME_CONFERENCIA'] = df_arquivar['NOME_COMPLETO_RAW']
df_final['CHAVE_USADA'] = df_arquivar['KEY_MATCH'] # Para você entender pq foi filtrado
df_final['DATA_ULTIMO_LOGIN'] = df_arquivar['ULTIMO_LOGIN']

# Ordenar por nome 
df_final = df_final.sort_values(by='NOME_CONFERENCIA')

output_filename = 'usuarios_para_suspender_smart_match.csv'
df_final.to_csv(output_filename, index=False)

print(f"Total encontrados para suspensão (Lógica Primeiro+Último): {len(df_final)}")
print(f"Arquivo gerado: {output_filename}")