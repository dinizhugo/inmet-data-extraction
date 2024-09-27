# Inmet Data Extractor

## Descrição do Projeto

Inmet Data Extractor é um script desenvolvido em Python que automatiza a extração de dados meteorológicos do site do INMET (Instituto Nacional de Meteorologia) e armazena esses dados em um banco de dados MongoDB. O objetivo é facilitar o monitoramento e análise de dados climáticos ao longo do tempo.

## Funcionalidades

- **Extração de Dados:** Captura dados meteorológicos de estações específicas para uma data ou período especificado.
- **Processamento de Dados:** Conversão e limpeza dos dados extraídos, incluindo tratamento de formatos numéricos e de datas.
- **Armazenamento em MongoDB:** Inserção dos dados processados em uma base de dados MongoDB para posterior análise.
  
## Tecnologias Utilizadas

- **Python:** Linguagem principal utilizada no desenvolvimento do script.
- **Selenium:** Automação de navegação e extração de dados do site.
- **BeautifulSoup:** Extração e parsing de dados HTML.
- **Pandas:** Manipulação e processamento dos dados em formato tabular.
- **MongoDB:** Banco de dados utilizado para armazenar os dados extraídos.
- **Chrome WebDriver:** Automação do navegador para acesso ao site do INMET.

## Estrutura do Projeto

- `InmetDataExtractor`: Classe principal responsável pela extração dos dados.
- `ProcessData`: Classe que processa e converte os dados extraídos para o formato necessário.
- `MongoDB`: Classe que gerencia a conexão e inserção dos dados no banco de dados MongoDB.

## Requisitos

- Python 3.8+
- MongoDB
- Google Chrome
- As seguintes bibliotecas Python:
  - `selenium`
  - `beautifulsoup4`
  - `pandas`
  - `pymongo`
  - `webdriver-manager`

## Instalação

1. Clone o repositório para o seu computador:

   ```bash
   git clone https://github.com/seu-usuario/inmet-data-extractor.git
   cd inmet-data-extractor
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Certifique-se de que o MongoDB está instalado e em execução na sua máquina local.

## Como Usar

### Extração de Dados para uma Única Data

Para extrair dados de uma estação para um dia anterior à data atual, utilize o método `extract_current_data`:

```python
extractor = InmetDataExtractor()
extractor.extract_current_data("nome_colecao", "numero_estacao")
```

### Extração de Dados para um Período

Para extrair dados de um período, utilize o método `extract_current_data_for_period`:

```python
extractor = InmetDataExtractor()
extractor.extract_current_data_for_period("nome_colecao", "numero_estacao", "01/01/2023", "10/01/2023")
```

#### Observações Importantes:

⚠️ **Atenção:**  
O método `extract_current_data_for_period()` é recomendável para períodos curtos de dias. Não utilize para grandes intervalos de tempo, pois isso pode causar sobrecarga na aplicação, aumentando o risco de falhas no processo de extração e processamento dos dados. Para períodos maiores, considere dividir a extração em intervalos menores para garantir a estabilidade e o desempenho da aplicação.


## Estrutura do Código

### `InmetDataExtractor`
- **`extract_current_data`:** Extrai dados para o dia anterior à data atual.
- **`extract_current_data_for_period`:** Extrai dados para um intervalo de datas.
- **`_extract_for_single_day`:** Métodos internos para extrair dados de um dia específico.
- **`_convert_data`:** Converte a tabela HTML extraída em um formato de dicionário JSON pronto para inserção no MongoDB.

### `ProcessData`
- **`process_data`:** Limpa e processa os dados convertidos, ajustando tipos e formatos.

### `MongoDB`
- **`insert_data_inmet`:** Insere os dados processados no banco de dados, evitando duplicatas.

## Possíveis Erros e Soluções

- **Erro de Conexão com o MongoDB:** Verifique se o MongoDB está em execução e acessível no endereço correto.
- **Elementos não encontrados pelo Selenium:** Certifique-se de que o layout do site do INMET não foi alterado e de que o ChromeDriver está atualizado.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para sugerir melhorias.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.
