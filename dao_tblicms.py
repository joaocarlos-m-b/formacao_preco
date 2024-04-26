from connection import SupabaseConnection

class TabelaICMS:
    def __init__(self) -> None:
        self.supabase = SupabaseConnection()

    def cadastrar_TabICMS (self, 
                     uf_origem:str, 
                     uf_destino:str, 
                     aliq_icms_nacional:float=0.0, 
                     aliq_icms_extrangeiro:float=0.0):
        if uf_destino == uf_origem:
            aliq_icms_extrangeiro=aliq_icms_nacional
        else:
            aliq_icms_extrangeiro=4
        
        if aliq_icms_extrangeiro < 1:
            aliq_icms_extrangeiro = aliq_icms_extrangeiro*100
        aliq_icms_extrangeiro = aliq_icms_extrangeiro
        
        dados = {
           'uf_origem':uf_origem,
           'uf_destino':uf_destino,
           'aliq_icms_nacional':aliq_icms_nacional,
           'aliq_icms_extrangeiro':aliq_icms_extrangeiro
        }
        return self.supabase.inserir('tabela_icms',dados)
    
    def pesquisar_TabICMS (self, columns='*', condition=None):
        if columns:
            if condition:
                results = self.supabase.pesquisar('tabela_icms', columns, condition)
            else:
                results = self.supabase.pesquisar('tabela_icms', columns)
        else:
            if condition:
                results = self.supabase.pesquisar('tabela_icms', '*', condition)
            else:
                results = self.supabase.pesquisar('tabela_icms')
        return results.data
    
    def excluir_TabICMS(self, condition):
        return self.supabase.excluir('tabela_icms', condition)

    def atualizar_TabICMS(self, dados, condition):
        return self.supabase.atualizar('tabela_icms', dados, condition)
    