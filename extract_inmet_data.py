from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import json
from util.process_data import ProcessData
from database.mongo import MongoDB

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InmetDataExtractor:
    def __init__(self) -> None:
        self.url = "https://tempo.inmet.gov.br/TabelaEstacoes"
        self.DB = MongoDB('mongodb://localhost:27017/')
        chrome_service = Service(ChromeDriverManager().install())

        self._driver = webdriver.Chrome(service=chrome_service)
        self._wait = WebDriverWait(self._driver, 20)
        
    def extract_current_data(self, collection_name: str, station_number:str):
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days = 1)
        self._extract_for_single_day(collection_name, station_number, datetime.strftime(date, "%d/%m/%Y"))
        
    
    def extract_current_data_for_period(self, collection_name:str, station_number: str, start_date: str, end_date: str):
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if datetime.strptime(start_date, '%d/%m/%Y') >= current_date or datetime.strptime(end_date, '%d/%m/%Y') >= current_date:
            print(f"[ERROR] Não é possivel escolher uma data maior ou igual que: {current_date.strftime('%d/%m/%Y')}")
            return

        start = datetime.strptime(start_date, '%d/%m/%Y')
        end = datetime.strptime(end_date, '%d/%m/%Y')

        for single_date in (start + timedelta(n) for n in range((end - start).days + 1)):
            date_str = single_date.strftime('%d/%m/%Y')
            print(f">> Extraindo dados para o dia: {date_str}")
            self._extract_for_single_day(collection_name,station_number, date_str)

    def _extract_for_single_day(self, collection_name:str, station_number: str, date: str):
        try:
            self._driver.get(f"{self.url}/{station_number}")
            sleep(3)

            menu_button = self._wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/i')))
            menu_button.click()

            start_date_input = self._wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div[4]/input')))
            start_date_input.clear()
            start_date_input.send_keys(date)

            end_date_input = self._wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div[5]/input')))
            end_date_input.clear()
            end_date_input.send_keys(date)

            generate_table_button = self._wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/button')))
            generate_table_button.click()

            self._wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'table')))

            page_source = self._driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            table = soup.find('table', attrs={'class': 'ui blue celled striped unstackable table'})
            
            json_data = self._convert_data(table, station_number, date)
            
            if json_data:
                # print(json.dumps(json_data, indent=4, ensure_ascii=False))
                self.DB.insert_data_inmet(collection_name, json_data)

        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
    
    def _convert_data(self, table, station_code, date) -> dict:
        try:
            data = {}
            rows = table.find_all('tr')
            daily_register = {
                "CODIGO": station_code,
                "DATA": datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d"),
                "MEDICOES": []
            }
            
            temp = []
            for row in rows[2:]:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols[1:]]
                temp.append(cols)

            df = pd.DataFrame(temp, columns=[
                'HORA', 'TEMP_BULBO_SECO', 'TEMP_MAX', 'TEMP_MIN', 'UMIDADE_RELATIVA', 
                'UMIDADE_RELATIVA_MAX', 'UMIDADE_RELATIVA_MIN', 'TEMP_PONTO_ORVALHO', 
                'TEMP_ORVALHO_MAX', 'TEMP_ORVALHO_MIN', 'PRESSAO_ATMOSFERICA_NIVEL_ESTACAO', 
                'PRESSAO_ATMOSFERICA_MAX', 'PRESSAO_ATMOSFERICA_MIN', 'VENTO_VELOCIDADE', 
                'VENTO_DIRECAO', 'VENTO_RAJADA_MAX', 'RADIACAO_GLOBAL', 'PRECIPITACAO_TOTAL'
            ])
            
            processor = ProcessData()
            df = processor.process_data(df)
            
            
            for record in df.to_dict(orient='records'):
                daily_register["MEDICOES"].append({k: v for k, v in record.items()})
            
            averages = df.mean(numeric_only=True).to_dict()
            for key, value in averages.items():
                daily_register[f"MEDIA_{key.upper()}"] = None if pd.isna(value) else value
            
            key = f"{station_code}_{datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")}"
            data[key] = daily_register
            
            return data

        except Exception as e:
            print(f"[ERROR] An error occurred while converting data: {e}")
