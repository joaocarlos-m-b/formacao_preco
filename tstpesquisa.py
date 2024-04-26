from dao_tblicms import TabelaICMS

tb = TabelaICMS()

uf_o = 'ES'
uf_d = 'SP'

dados = tb.pesquisar_TabICMS(condition={'uf_origem': uf_o, 'uf_destino': uf_d})
if dados:  # Verifica se a lista não está vazia
    aliq_icms_nacional = dados[0]['aliq_icms_nacional']
    aliq_icms_extrangeiro = dados[0]['aliq_icms_extrangeiro']
    print(f'Aliquota ICMS Nacional: {aliq_icms_nacional}%')
    print(f'Aliquota ICMS Estrangeiro: {aliq_icms_extrangeiro}%')
else:
    print("Nenhum dado encontrado para as UFs especificadas.")

    '''
    Neste trecho de código:

    dados[0] acessa o primeiro item da lista, que é o dicionário contendo os dados.
    dados[0]['aliq_icms_nacional'] e dados[0]['aliq_icms_extrangeiro'] 
    acessam respectivamente as alíquotas nacional e estrangeira de ICMS.
    
    '''
