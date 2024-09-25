import pandas as pd
from datetime import datetime

class ProcessData:
    def __init__(self) -> None:
        self.DEFAULT_COLUMNS = [
            'DATA', 'HORA', 'TEMP_BULBO_SECO', 'TEMP_MAX', 'TEMP_MIN', 'UMIDADE_RELATIVA', 
            'UMIDADE_RELATIVA_MAX', 'UMIDADE_RELATIVA_MIN', 'TEMP_PONTO_ORVALHO', 
            'TEMP_ORVALHO_MAX', 'TEMP_ORVALHO_MIN', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO', 
            'PRESSAO_ATMOSFERICA_MAX', 'PRESSAO_ATMOSFERICA_MIN', 'VENTO_VELOCIDADE', 
            'VENTO_DIRECAO', 'VENTO_RAJADA_MAX', 'RADIACAO_GLOBAL', 'PRECIPITACAO_TOTAL'
        ]
    
    def process_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        columns_name = self.DEFAULT_COLUMNS
        
        dataframe = dataframe.iloc[:, :len(columns_name)]
        dataframe.columns = columns_name
        
        columns_to_numeric = [
            'TEMP_BULBO_SECO', 'TEMP_MAX', 'TEMP_MIN', 'UMIDADE_RELATIVA',
            'UMIDADE_RELATIVA_MAX', 'UMIDADE_RELATIVA_MIN', 'TEMP_PONTO_ORVALHO', 
            'TEMP_ORVALHO_MAX', 'TEMP_ORVALHO_MIN', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO',
            'PRESSAO_ATMOSFERICA_MAX', 'PRESSAO_ATMOSFERICA_MIN', 'VENTO_VELOCIDADE', 
            'VENTO_DIRECAO', 'VENTO_RAJADA_MAX', 'RADIACAO_GLOBAL', 'PRECIPITACAO_TOTAL'
        ]
        
        for column in columns_to_numeric:
            dataframe[column] = pd.to_numeric(dataframe[column].str.replace(',', '.'), errors='coerce')
        
     
        columns_to_int = [
            'UMIDADE_RELATIVA_MAX',
            'UMIDADE_RELATIVA_MIN',
            'UMIDADE_RELATIVA',
            'VENTO_DIRECAO'
        ]
        
        for column in columns_to_int:
            dataframe[column] = pd.to_numeric(dataframe[column], downcast='integer', errors='coerce')
        
        dataframe['DATA'] = pd.to_datetime(dataframe['DATA'], format="%d/%m/%Y").dt.strftime("%Y/%m/%d")
        dataframe['HORA'] = dataframe['HORA'].astype(str) + ' UTC'
        
        return dataframe
