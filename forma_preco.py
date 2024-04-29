from dataclasses import dataclass
from dao_tblicms import TabelaICMS

@dataclass
class FormacaoPreco:
    preco_compra: float = 0.0
    pFrete: float = 0.0
    pIpiCusto: float = 0.0
    pOutrosCustos: float = 0.0
    pICMSR: float = 0.0
    pCredICMS: float = 0.0
    pCredPis: float = 0.0
    pCredCofins: float = 0.0
    pTributos: float = 0.0
    pComissao: float = 0.0
    pDiretas: float = 0.0
    pIndiretas: float = 0.0
    pOperacionais: float = 0.0
    pMargem: float = 0.0
    uf_Origem: str = None
    uf_Destino: str = None
    pMVA: float = 0.0
    pIpiVenda: float = 0.0
    pAliqIcmsMenorRed: float = 0.0
    possuiSt: bool = False
    pDifVistaPrazo: float = 0.0
    tbIcms: TabelaICMS = TabelaICMS()

    def __post_init__(self):
        self.validate_ufs()
        self.fetch_icms_rates()
        self.convert_percentage_to_decimal()

    def validate_ufs(self):
        if not self.uf_Origem or self.uf_Origem.upper() not in self.valid_ufs():
            raise ValueError("Favor informar uma UF de origem válida")
        if not self.uf_Destino or self.uf_Destino.upper() not in self.valid_ufs():
            raise ValueError("Favor informar uma UF de destino válido")

    @staticmethod
    def valid_ufs():
        return ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 
                'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RN', 'RS', 'RJ', 'RO', 'RR', 'SC', 
                'SP', 'SE', 'TO']

    def fetch_icms_rates(self):
        conditions = {'uf_origem': self.uf_Origem.upper(), 'uf_destino': self.uf_Destino.upper()}
        result = self.tbIcms.pesquisar_TabICMS(condition=conditions)
        self.aliqICMS = result[0]['aliq_icms_nacional'] / 100
        if self.possuiSt:
            self.aliqST = result[0]['aliq_icms_nacional'] / 100  # Suposição sobre onde buscar a aliquota ST

    def convert_percentage_to_decimal(self):
        for field in ['pFrete', 'pIpiCusto', 'pOutrosCustos', 'pICMSR', 'pCredICMS',
                      'pCredPis', 'pCredCofins', 'pTributos', 'pComissao', 'pDiretas',
                      'pIndiretas', 'pOperacionais', 'pMargem', 'pMVA', 'pIpiVenda', 'pAliqIcmsMenorRed', 'pDifVistaPrazo']:
            setattr(self, field, getattr(self, field) / 100)

    def calc_valor_contabil(self):
        return self.preco_compra * (1 + self.pFrete + self.pIpiCusto + self.pOutrosCustos + self.pICMSR)

    def calc_valor_custo(self):
        valorCusto =  (self.preco_compra * (1 + self.pFrete 
                                              + self.pIpiCusto 
                                              + self.pOutrosCustos
                                              + self.pICMSR
                                              - self.pCredICMS
                                              - self.pCredPis
                                              - self.pCredCofins))
        return valorCusto

    def calc_custo_comercializacao(self):
        custo = self.calc_valor_custo()
        custoComercializacao = custo / (1-( self.pTributos
                                           +self.pComissao
                                           +self.pDiretas
                                           +self.pIndiretas
                                           +self.pOperacionais))
        return custoComercializacao
    
    def preco_vista(self):
        custo = self.calc_valor_custo()
        precoV = custo / (1-( self.pTributos
                                           +self.pComissao
                                           +self.pDiretas
                                           +self.pIndiretas
                                           +self.pOperacionais
                                           +self.pMargem))
        return precoV
    
    def preco_prazo(self):
        precoV = self.preco_vista()
        precoP = precoV * (1 + self.pDifVistaPrazo)

        return precoP
    
    def margem_lucro_bruto(self):
        precoV = self.preco_vista()
        custoComercializacao =self.calc_custo_comercializacao()

        MargemLucroBruto = (precoV-custoComercializacao)/custoComercializacao

        mlb = MargemLucroBruto*100

        return mlb

    def reversao_valores(self):
        precoV = self.preco_vista()
        precoP = self.preco_prazo()
        custoCom = self.calc_custo_comercializacao()

        pbaseVrIPI = (1 + self.pIpiVenda)
        pbaseBCST = (1 + self.pMVA)*pbaseVrIPI
        if self.possuiSt:
            pbasePICMSST = (pbaseBCST*self.aliqST)-self.aliqICMS
        else:
            pbasePICMSST = 0

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
    
    