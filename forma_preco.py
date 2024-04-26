
from dao_tblicms import TabelaICMS

class FormacaoPreco():

    def __init__(self, 
                    preco_compra=0.0, 
                    pFrete=0.0,
                    pIpiCusto = 0.0, 
                    pOutrosCustos=0.0,
                    pICMSR=0.0,
                    pCredICMS=0.0,
                    pCredPis=0.0,
                    pCredCofins=0.0,
                    pTributos=0.0,
                    pComissao=0.0,
                    pDiretas=0.0,
                    pIndiretas=0.0,
                    pOperacionais=0.0,
                    pMargem=0.0,
                    uf_Origem:str=None,
                    uf_Destino:str=None,
                    pMVA=0.0,
                    pIpiVenda=0.0,                   
                    pAliqIcmsMenorRed=0.0,
                    possuiSt:bool=False,
                    pDifVistaPrazo=0.0):
        
        self.tbIcms = TabelaICMS()
        
        UF:list = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 
          'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 
          'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
          'RN', 'RS', 'RJ', 'RO', 'RR', 'SC', 
          'SP', 'SE', 'TO']
        
        if preco_compra <= 0.0:
            raise ValueError("Favor informar um valor maior que zero!")

        if uf_Destino is None:
            raise ValueError("Favor informar uma UF de destino válido")
        
        if uf_Origem is None:
            raise ValueError("Favor informar uma UF de origem válida")

        if uf_Destino.upper() not in UF:
            raise ValueError("Favor informar uma UF de destino válido")

        if uf_Origem.upper() not in UF:
            raise ValueError("Favor informar uma UF de origem válida")
        
        dado_aliqST=self.tbIcms.pesquisar_TabICMS(condition={'uf_origem':uf_Destino.upper(),
                                                        'uf_destino':uf_Destino.upper()})
        dado_aliqICMS=self.tbIcms.pesquisar_TabICMS(condition={  'uf_origem':uf_Origem.upper(),
                                                            'uf_destino':uf_Destino.upper()})
        aliqST:float = (dado_aliqST[0]['aliq_icms_nacional'])/100
        aliqICMS:float = (dado_aliqICMS[0]['aliq_icms_nacional'])/100

        if (pAliqIcmsMenorRed/100) >= aliqICMS or pAliqIcmsMenorRed < 0:
            if (pAliqIcmsMenorRed/100) >= aliqICMS:
                raise ValueError(f'O valor da alíquota menor de ICMS para redução ({pAliqIcmsMenorRed} %)\
                                 é maior que a alíquota de ICMS passível da operação ({aliqICMS*100} %).\
                                 Favor verificar para evitar erros na apuração')
            else:
                raise ValueError(f'O valor da alíquota menor de ICMS para redução ({pAliqIcmsMenorRed} %)\
                                 é menor que zero. Favor revisar, e caso não tiver, deixe zero')




        self.aliqST = aliqST
        self.aliqICMS = aliqICMS       
        self.preco_compra = preco_compra
        self.pFrete = pFrete/100
        self.pIpiCusto = pIpiCusto/100
        self.pOutrosCustos = pOutrosCustos/100
        self.pICMSR = pICMSR/100
        self.pCredICMS = pCredICMS/100
        self.pCredPis = pCredPis/100
        self.pCredCofins = pCredCofins/100
        self.pTributos = pTributos/100
        self.pComissao = pComissao/100
        self.pDiretas = pDiretas/100
        self.pIndiretas = pIndiretas/100
        self.pOperacionais = pOperacionais/100
        self.pMargem = pMargem/100
        self.uf_Origem = uf_Origem.upper()
        self.uf_Destino = uf_Destino.upper()
        self.pMVA = pMVA/100
        self.pIpiVenda = pIpiVenda/100        
        self.pAliqIcmsMenorRed = pAliqIcmsMenorRed/100
        self.possuiSt = possuiSt
        self.pDifVistaPrazo = pDifVistaPrazo/100

    def calcValorContabil(self):
        valorContabil = (self.preco_compra * (1 + self.pFrete 
                                              + self.pIpiCusto 
                                              + self.pOutrosCustos
                                              + self.pICMSR))
        return valorContabil
    
    def calcValorCusto(self):
        valorCusto =  (self.preco_compra * (1 + self.pFrete 
                                              + self.pIpiCusto 
                                              + self.pOutrosCustos
                                              + self.pICMSR
                                              - self.pCredICMS
                                              - self.pCredPis
                                              - self.pCredCofins))
        return valorCusto
    
    def calcCustoComerc(self):
        custo = self.calcValorCusto()
        custoComercializacao = custo / (1-( self.pTributos
                                           +self.pComissao
                                           +self.pDiretas
                                           +self.pIndiretas
                                           +self.pOperacionais))
        return custoComercializacao
    
    def precoVista(self):
        custo = self.calcValorCusto()
        precoV = custo / (1-( self.pTributos
                                           +self.pComissao
                                           +self.pDiretas
                                           +self.pIndiretas
                                           +self.pOperacionais
                                           +self.pMargem))
        return precoV
    
    def precoPrazo(self):
        precoV = self.precoVista()
        precoP = precoV * (1 + self.pDifVistaPrazo)

        return precoP
    
    def pMargemLucroBruto(self):
        precoV = self.precoVista()
        custoComercializacao =self.calcCustoComerc()

        MargemLucroBruto = (precoV-custoComercializacao)/custoComercializacao

        mlb = MargemLucroBruto*100

        return mlb
    
    def reversaoValores(self):        
        
        precoV = self.precoVista()
        precoP = self.precoPrazo()
        custoCom = self.calcCustoComerc()

        pbaseVrIPI = (1 + self.pIpiVenda)
        pbaseBCST = (1 + self.pMVA)*pbaseVrIPI
        pbasePICMSST = (pbaseBCST*self.aliqST)-self.aliqICMS
        pbaseTotalNF = 1 + pbasePICMSST + self.pIpiVenda
       

        if self.possuiSt:
            ValorAVista = precoV/(pbaseTotalNF)
            ValorAPrazo = precoP/(pbaseTotalNF)
            pLucro = ((ValorAVista-custoCom)/custoCom)*100
        else:
            ValorAVista = precoV/(1+self.pIpiVenda)
            ValorAPrazo = precoP/(1+self.pIpiVenda)
            pLucro = ((ValorAVista-custoCom)/custoCom)*100
        return{'preco_vista':ValorAVista, 'preco_prazo': ValorAPrazo, 'pLucro': pLucro}







        

    



    





        



















        

   
        
        