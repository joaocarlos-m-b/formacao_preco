import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client

class SupabaseConnection:
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.conn: Client = self.create_client()

    def create_client(self):
        return create_client(self.url, self.key)
        
    def pesquisar(self, table_name, columns="*", condition=None):
        if condition:
            if type(condition) is tuple:
                return self.conn.table(table_name).select(*columns).eq(*condition).execute()
            if type(condition) is dict:
                return self.conn.table(table_name).select(*columns).match(condition).execute()
            None
        else:
            return self.conn.table(table_name).select(*columns).execute()
        
    def excluir(self, table_name, condition=None):
        return self.conn.table(table_name).delete().eq(*condition).execute()        
        
    def atualizar(self, table_name, dados, condition):
        return  self.conn.table(table_name).update(dados).eq(*condition).execute()        
    
    def inserir(self, table_name, dados):
        return self.conn.table(table_name).insert(dados).execute()
        

