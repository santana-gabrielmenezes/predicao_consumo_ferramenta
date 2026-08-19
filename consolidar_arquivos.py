# importa bibliotecas necessárias para a execução do script
import os
import glob
import pandas as pd

# busca arquivos com um prefixo especifico em um diretório especificado, concatena e exporta com um nome predefinido
def consolidar_arquivos(diretorio_entrada, diretorio_saida, prefixo_busca, nome_arquivo_saida, colunas, numero_linhas_finais): # cria função para buscar arquivos a serem consolidados
    padrao = os.path.join(diretorio_entrada, f'{prefixo_busca}*.csv') # define o padrão de diretório + nome para os arquivos a serem consolidados
    arquivos = glob.glob(padrao) # cria uma lista com o caminho de todos os arquivos que se enquadrarem na regra da variável `padrao`

    if not arquivos: # cria um condicional para caso não sejam encontrados arquivos no padrão `padrao`
        print(f'Nenhum arquivo encontrado no padrão {padrao}') # exibe mensagem de aviso para nenhum arquivo encontrado
        return # sem retorno no condicional

    lista_dfs = [] # inicia a lista de dfs

    print(f'Inciando consolidação de arquivos no padrão {padrao} ({len(arquivos)} arquivos)') # exibe uma mensagem de início da consolidação

    for arquivo in arquivos: # inicia um loop para concatenação dos arquivos
        df = pd.read_csv(arquivo, low_memory=False) # cria um df temporário com os dados do arquivo no caminho definido em `arquivo` nesta iteração
        df = df[colunas] # elimina todas as colunas desnecessárias
        df = df.iloc[:-numero_linhas_finais] # elimina as últimas linhas do df (linhas de somatórios originárias do SAP)
        lista_dfs.append(df) # insere cada df em uma lista de dfs

    df_consolidado = pd.concat(lista_dfs, ignore_index=True) # concatena todos os dfs da lista_dfs em um único df

    caminho_saida = os.path.join(diretorio_saida, nome_arquivo_saida) # define o nome e o diretorio onde o arquivo consolidado será salvo

    df_consolidado.to_parquet(caminho_saida, index=False) # exporta o arquivo em .parquet

    print(f'Arquivo gerado com sucesso: {nome_arquivo_saida}') # exibe uma mensagem de sucesso

# execulta a função de consolidação
if __name__ == '__main__': # cria um condicional que só execulta o script se este for execultado diretamente (como programa principal)
    diretorio_dados = 'dados_originais' # define o diretório onde execultar a busca

    if not os.path.exists(diretorio_dados): # cria um condicional para caso o diretório não exista
        print(f'Erro: diretório {diretorio_dados} não encontrado.') # exibe uma mensagem de erro caso o diretório não exista
    else:
        consolidar_arquivos( # execulta a função de consolidação nos parâmetros abaixo
            diretorio_entrada=diretorio_dados, # define o diretório com os dados a serem consolidados
            diretorio_saida='', # define o diretório para o arquivo com os dados já consolidados
            prefixo_busca='tb_producao_', # define o prefixo dos arquivos
            nome_arquivo_saida='tb_producao_consolidado.parquet', # define o nome de saída do arquivo
            colunas=['Material', 'Qtd.boa confirm.', 'Dt.lçto.'], # define as colunas a serem mantidas no df
            numero_linhas_finais=3 # define o número de linhas a ser descartada no fim de cada arquivo original
        )
        consolidar_arquivos( # execulta a função de consolidação nos parâmetros abaixo
            diretorio_entrada=diretorio_dados, # define o diretório com os dados a serem consolidados
            diretorio_saida='', # define o diretório para o arquivo com os dados já consolidados
            prefixo_busca='tb_consumo_ferramentas_', # define o prefixo dos arquivos
            nome_arquivo_saida='tb_consumo_ferramentas_consolidado.parquet', # define o nome de saída do arquivo
            colunas=['Material', 'Qtd.  UM registro', 'Data de lançamento'], # define as colunas a serem mantidas no df
            numero_linhas_finais=7 # define o número de linhas a ser descartada no fim de cada arquivo original
        )