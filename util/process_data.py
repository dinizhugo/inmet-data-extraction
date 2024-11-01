import pandas as pd

class ProcessData:
    def __init__(self) -> None:
        self.DEFAULT_COLUMNS = [
            'HORA', 'TEMP_BULBO_SECO', 'TEMP_MAX', 'TEMP_MIN', 'UMIDADE_RELATIVA', 
            'UMIDADE_RELATIVA_MAX', 'UMIDADE_RELATIVA_MIN', 'TEMP_PONTO_ORVALHO', 
            'TEMP_ORVALHO_MAX', 'TEMP_ORVALHO_MIN', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO', 
            'PRESSAO_ATMOSFERICA_MAX', 'PRESSAO_ATMOSFERICA_MIN', 'VENTO_VELOCIDADE', 
            'VENTO_DIRECAO', 'VENTO_RAJADA_MAX', 'RADIACAO_GLOBAL', 'PRECIPITACAO_TOTAL'
        ]
        
        self.COLUMNS_TO_NUMERIC = [
            'PRECIPITACAO_TOTAL', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO', 'PRESSAO_ATMOSFERICA_MAX', 
            'PRESSAO_ATMOSFERICA_MIN', 'RADIACAO_GLOBAL', 'TEMP_BULBO_SECO', 'TEMP_PONTO_ORVALHO', 
            'TEMP_MAX', 'TEMP_MIN', 'TEMP_ORVALHO_MAX', 'TEMP_ORVALHO_MIN', 'VENTO_RAJADA_MAX', 
            'VENTO_VELOCIDADE', 'UMIDADE_RELATIVA_MAX', 'UMIDADE_RELATIVA_MIN', 
            'UMIDADE_RELATIVA', 'VENTO_DIRECAO'
        ]
    
    def process_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.iloc[:, :len(self.DEFAULT_COLUMNS)]
        dataframe.columns = self.DEFAULT_COLUMNS
        
        for column in self.COLUMNS_TO_NUMERIC:
            dataframe[column] = pd.to_numeric(dataframe[column].str.replace(',', '.'), errors='coerce')
        
        dataframe['HORA'] = dataframe['HORA'].astype(str) + ' UTC'
        
        dataframe = dataframe.map(lambda x: None if pd.isna(x) else x)
        
        return dataframe
