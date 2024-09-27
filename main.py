from extract_inmet_data import InmetDataExtractor
import schedule
from time import sleep

extrator = InmetDataExtractor()

def tarefa():
    print(">> Realizando tarefa...")
    # extrator.extract_current_data_for_period("2024", "A310", "20/09/2024", "20/09/2024")
    extrator.extract_current_data("2024", "A310")

# schedule.every(10).seconds.do(tarefa)
schedule.every(1).days.do(tarefa)

while 1:
    schedule.run_pending()
    sleep(1)