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
resultado = fp.reversaoValores()

# Imprimir o resultado
print(resultado)
