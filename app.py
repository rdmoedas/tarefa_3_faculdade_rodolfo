import mysql.connector
from mysql.connector import Error

# Objetivo, responder essas três perguntas obtendo dados de um banco de dados.

    # ! a) qual o maior e o menor índice de acidentes de trânsito e a que cidades pertencem
    # ! b) qual a média de veículos nas cidades juntas;
    # ! c) qual a média de acidentes de trânsito nas cidades com menos de 2000 veículos de passeio.

# Como não encontrei nada pronto consultei duas fontes diferentes e montei um banco de dados com os dados necessários para o exercício.
# Do IBGE obtive a população total das cidades
# Do DETRAN Parana obtive a quantidade de veiculos separadas por tipos, utilizando o excel cheguei ao dado de veiculos de passeio (considerei automoveis, motos e motonetas)
# Também do DETRAN Parana obtive o número total de acidentes com vítimas em cada uma das cidades. Observação, algumas cidades pequenas não tinham esse dado, então tive que procurar as que possuiam.

# Com esses dados planilhados montei um banco de dados MySQL no heroku para que ele fica-se disponivel para o tutor utilizar durante a correção.
# Embora não seja uma boa prática tive que deixar os dados de acesso no código já que não sabia como passar um .env utilizando o sistema da faculdade.

#########
## ! Função para conexão com o banco de dados.
## ! Ela recebe uma query e retorna o resultado dessa query.
## Função baseada nesse exemplo: https://pynative.com/python-mysql-database-connection/
def dados_cidades_parana(query):
    records = ''
    try:
        connection = mysql.connector.connect(
            host='ADICIONAR_O_ENDEREÇO_DO_HOST',
            database='NOME_DA_DATABASE',
            user='USUARIO',
            password='SENHA'
        )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute(query)

            # retorna todos os resultados
            records = cursor.fetchall()

    except Error as e:
        print("Erro durante conexão ao Banco MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("Conexão com MySQL foi fechada")

        return records

# Aqui seleciono todos os dados da tabela cidades_transito
data = dados_cidades_parana("SELECT * FROM cidades_transito")

print("DADOS OBTIDOS UTILIZANDO O IBGE E O DETRAN PR COMO FONTE")

def imprimi_dados(dados):
    legenda = ("Cód cidade", "Nome Cidade", "Estado", "População Total", "Veiculos de Passeio", "Número de Acidentes com Vitima")
    print(legenda)
    for i in dados:
        print(i)
imprimi_dados(data)

    # ! Resposta simples do item A
    # ! Essa foi a resposta que cheguei inicialmente para o item A, mas refiz o exercício pensando em aprofundar no assunto.
# data = dados_cidades_parana("SELECT * FROM cidades_transito ORDER BY total_acidentes_transito_vitimas DESC")
# print('Maior indice de transito é de: ', data[0][1])
# print('Menor indice de transito é de: ', data[len(data) - 1][1])

    # ! Resposta mais elaborada do item A

# Calcula o indice de transito dividindo o número de acidentes pelo tamanho da população.
# Pelo enunciado do problema não soube dizer qual era a forma de calcular o indice de transito, mas acredito que dessa forma é fácil trocar os valores e realizar um novo calculo...
# sem afetar muito a lógica utilizada no programa.
# Indice de transito é calculado e salvo em uma nova lista.
# O indice foi multiplicado por 100 e arredondado para 3 casas para facilitar a leitura.
def calcula_indice_transito(arr):
    new_arr = []
    for i in arr:
        new = i[5] / i[3]
        new = new * 100
        item = (i[0], i[1], i[2], i[3], i[4], i[5], round(new, 3))
        new_arr.append(item)
    return new_arr

# Salva a nova lista na variavel novos_dados
novos_dados = calcula_indice_transito(data)

# Organiza a lista utilizando o metodo sort, usa como referencia o indice de transito.
# Depois de algumas tentativas utilizei essa resposta como modelo https://stackoverflow.com/questions/14829300/python-tuples-sorting-based-on-last-element
novos_dados.sort(key=lambda x: x[6])

print("RESPOSTA A")
print("O Maior indice de transito é da cidade: ", novos_dados[len(novos_dados) - 1][1])

print("O Menor indice de transito é da cidade: ", novos_dados[0][1])

#  Resposta do ITEM B e C
# Aqui utilizei as query MySQL para realizar o calculo das médias e o filtro por valores
# Essa foi a referencia utilizada https://www.mysqltutorial.org/mysql-max-function/
print("RESPOSTA B")
media_veiculos = dados_cidades_parana("SELECT AVG(total_veiculos_passeio) AS media_carros_todas_cidades FROM cidades_transito")
print('A média de veiculos em todas as cidades é: ', round(media_veiculos[0][0], 2))    # Deve retornar 3347

print("RESPOSTA C")
media_acidentes_pequenas_cidades = dados_cidades_parana("SELECT AVG(total_veiculos_passeio) AS media_carros_todas_cidades FROM cidades_transito WHERE total_veiculos_passeio < 2000")
print('A média de veiculos nas cidades com menos de 2000 veiculos de passeio é: ', round(media_acidentes_pequenas_cidades[0][0], 2))  # Deve retornar 1480
