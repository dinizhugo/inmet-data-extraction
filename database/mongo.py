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
    
    def insert_data_inmet(self, collection_name:str, key:str, data:dict):
        collection = self.get_collection(collection_name)
        station = collection.find_one({"CODIGO": key})
        
        if not station:
            print(f"Estação com código {key} não encontrada!")
            return
        
        existing_data = station.get("DADOS", [])

        # Verifica se o valor de "HORA" do novo dado já está presente
        for record in existing_data:
            if record["HORA"] == data["HORA"] and record["DATA"] == data["DATA"]:
                print(f"Dados para a hora {data['HORA']} e data {data['DATA']} já existem.")
                return
        
        # Se não houver duplicata, insere o novo dado
        collection.update_one(
            {"CODIGO": key},
            {"$push": {"DADOS": data}}
        )
        print(f"Novo dado inserido para a estação {key}: {data['DATA']} {data['HORA']}")