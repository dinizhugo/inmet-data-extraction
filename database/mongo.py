from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError


class MongoDB:
    def __init__(self, connection_string):
        try:
            self.__client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            self.__client.admin.command('ping')
            print(">> Conexão com o MongoDB estabelecida com sucesso!\n")

            self.DB = 'projeto_valnyr'
        except ConnectionFailure as e:
            print("[ERROR] Não foi possivel se conectar com o banco de dados.\n")

    def get_data_base(self):
        if self.__client:
            db = self.__client[self.DB]
            return db
        else:
            print("[ERROR] Acesso ao banco de dados falhou. Conexão não estabelecida. \n")            
            return None
    
    def get_collection(self, name):
        collection_name = str(name)
        db = self.get_data_base()
        if db is not None:
            return db[collection_name]
        else:
            print("[ERROR] Não foi possível acessar a coleção com esse nome.\n")
            return None
    
    def insert_data_inmet(self, collection_name:str, data:dict):
        collection = self.get_collection(collection_name)
        
        if collection is not None:
            try:
                documentos = []
                for chave, valor in data.items():
                    documento = valor
                    documento['_id'] = chave
                    documentos.append(documento)
                
                print("Inserindo dados...")
                collection.insert_many(documentos)
                print(f">> O documento foi inserido no banco {collection_name}.\n")
            except Exception as e:
                print(f"Erro ao inserir os dados: {str(e)}")
        print("============================================")