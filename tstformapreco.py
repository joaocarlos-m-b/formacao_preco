from forma_preco import FormacaoPreco

# Criar uma instância da classe FormacaoPreco com os valores desejados
fp = FormacaoPreco(
                    preco_compra=44.17, 
                    pFrete=3.6640,
                    pIpiCusto = 0.0, 
                    pOutrosCustos=20.0,
                    pICMSR=15.0,
                    pCredICMS=7.0,
                    pCredPis=1.65,
                    pCredCofins=7.60,
                    pTributos=25.5,
                    pComissao=2.0,
                    pDiretas=0.0,
                    pIndiretas=0.0,
                    pOperacionais=33.0,
                    pMargem=16.9470,
                    uf_Origem='es',
                    uf_Destino='es',
                    pMVA=70.0,
                    pIpiVenda=5.0,                                     
                    pAliqIcmsMenorRed=0.0,
                    possuiSt=True,
                    pDifVistaPrazo=5.0
)

# Chamar o método reversaoValores para obter os dados desejados
resultado = {
    'valor_contabil':round(fp.calc_valor_contabil(),2), 
    'custo_mercadoria':round(fp.calc_valor_custo(),2),   
    'custocomercializacao': round(fp.calc_custo_comercializacao(),2),
    'produto_st':fp.possuiSt,
    'reversao':fp.reversao_valores()}

# Acessando o valor de pLucro dentro do dicionário resultado
p_lucro = resultado['reversao']['pLucro']

# Imprimir o valor de pLucro
print(p_lucro)



'''
for resultado in resultados:
    p_lucro = resultado['reversao']['pLucro']
    print(p_lucro)

'''