import pandas as pd
from dao_tblicms import TabelaICMS

tb = TabelaICMS()
file_path = 'tab_icms.xlsx'

df = pd.read_excel(file_path,header=0,index_col=0)

# Iterando linha coluna

for origem, linha in df.iterrows():
    for destino, aliq_icms_nacional in linha.items():
        # print(f'UF Orig: {origem}, UF Dest: {destino} = ICMS de: {aliq_icms_nacional}')
        tb.cadastrar_TabICMS(origem,destino,aliq_icms_nacional*100)