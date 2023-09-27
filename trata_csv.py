# Bruno Nascimento - 27-09-2023
# Ferramenta Python para arquivos texto ou csv
# Funcao tratar_arquivo_csv trata arquivos para serem carregados na carga mensal
# Funcao converter_csv_para_sql deixa um arquivo para inserts pronto para bulk insert

import csv

def tratar_arquivo_csv(arquivo_entrada, arquivo_saida, campo_num):
    """
    Trata um arquivo .csv retirando espaços '' ou ' ' e substituindo campos vazios por NULL.

    Args:
        arquivo_entrada: O caminho para o arquivo de entrada.
        arquivo_saida: O caminho para o arquivo de saída.

    Returns:
        Nenhum.
    """
    # Abre o arquivo de entrada em modo de leitura.
    with open(arquivo_entrada, "r", encoding="utf8", errors="ignore") as f_entrada:
        # Cria um leitor de CSV.
        reader = csv.reader(f_entrada, delimiter=";")

        # Pula a linha de cabeçalho.
        next(reader, None)

        # Cria um arquivo de saída em modo de escrita.
        with open(arquivo_saida, "w", newline='') as f_saida:
            # Inicializa o escritor de CSV.
            writer = csv.writer(f_saida, delimiter=",")

            # Itera sobre as linhas do arquivo de entrada.
            for linha in reader:
                # Substitui campos vazios entre ;; por ,NULL,
                linha = [campo.strip() if campo.strip() else "NULL" for campo in linha]

                # Transforma campos '00000000' por #.
                linha = ["#" if campo == "00000000" else campo for campo in linha]

                # Escreve a linha tratada no arquivo de saída com aspas simples envolvendo os valores.
                writer.writerow([campo if ((campo == 'NULL' or campo == linha[campo_num]) and campo != '#') else "'" + campo + "'" for campo in linha])

def converter_csv_para_sql(arquivo_csv, arquivo_sql, nome_da_tabela):
  """
  Converte um arquivo CSV tratado em INSERT SQL.

  Args:
    arquivo_csv: O caminho para o arquivo CSV tratado.
    nome_da_tabela: O nome da tabela para a qual as linhas do CSV serão inseridas.

  Returns:
    O código SQL para inserir as linhas do CSV na tabela.
  """

  # Abre o arquivo CSV tratado em modo de leitura.
  with open(arquivo_csv, "r") as f_csv:
    # Cria um leitor de CSV.
    reader = csv.reader(f_csv, delimiter=",")

    # Itera sobre as linhas do CSV.
    linhas = []
    linhas.append(f"INSERT INTO {nome_da_tabela} VALUES ")
    linhas.append("\n")
    for linha in reader:
      # Monta a instrução INSERT SQL.
      linhas.append(f"({','.join(linha)})")
      linhas.append(",")
      linhas.append("\n")
    linhas.pop()
    linhas.pop()
    linhas.append(';')

  # Cria o arquivo SQL.
  with open(arquivo_sql, "w") as f_sql:
    f_sql.writelines(linhas)

# usos apos o carregamento das funcoes idle ou jupyter
# caminhos DOS devem usar "/"

# Caminho arquivo entrada
arquivo_entrada = "C:/Users/bruno.artagoitia/Documents/CARGAS/Tratador de csv/teste.csv" 

# Caminho arquivo saida
arquivo_saida = "C:/Users/bruno.artagoitia/Documents/CARGAS/Tratador de csv/teste_tratado.csv"

# gera arquivo tratado - (arquivo_entrada,arquivo_saida, numero campo sem aspas de 0 a n)
tratar_arquivo_csv(arquivo_entrada,arquivo_saida,1)

# Caminho arquivo SQL
arquivo_sql = "C:/Users/bruno.artagoitia/Documents/CARGAS/Tratador de csv/saida.sql"

# gera arquivo SQL INSERT pronto - (arquivo_saida, arquivo_sql, string nome da tabela com ou sem campos entre parenteses)
converter_csv_para_sql(arquivo_saida, arquivo_sql, "sch_sad.sad_cargo")