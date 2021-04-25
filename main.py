from ConexaoBD import *
from WorkbookUtil import *

BD = ConexaoBD()
workbook = WorkbooktUtil()


while True:
    
    print('{:-^50}'.format('MENU'))
    print(
'''
(1) Gerar planilha
(2) Adminstração do Banco de Dados
(3) ?????????
(0) Fechar programa
''')

    escolha = int(input("Digite o número da opção desejada e tecle Enter: "))

    if escolha == 1:
        while True:
            print('''(1) Colar consulta pronta
                    (2) Selecionar tabela, colunas e condições
                    (0) Voltar ao menu anterior''')
            escolha = int(input("Digite o número da opção desejada e tecle Enter: "))

            if escolha == 1:
                workName = input("Escolha um nome para o arquivo da planilha:\n")
                with BD.conectarBanco() as dataBaseCon:         
                    cursor = dataBaseCon.cursor()
                    cursor.execute(input("Cole a consulta que você quer na planilha e tecle Enter\n")) 
                    result =  cursor.fetchall()
                    colNames = [i[0] for i in cursor.description]

                    workbook.createWorkbook(result, workName, colNames)

            elif escolha == 0:
                break

                    
    if escolha == 2:

        while True:
            print('{:-^50}'.format('ADMINISTRAÇÃO BD'))
            print('(1) Visualizar conexões existentes\n'+
                '(2) Visualizar conexão selecionada (padrão)\n' +
                '(3) Adicionar nova Conexão\n'+
                '(4) Remover conexão\n'+
                '(0) Voltar ao menu\n')

            escolha = int(input())


            if escolha == 1:
                for conexao in BD.conexoes.keys():
                    conex_aux = BD.conexoes[conexao]
                    print('='*50)
                    print('Nome da conexão: ', conexao)
                    print('Usuário: ', conex_aux['usuario'])
                    print('IP do Banco: ', conex_aux['IP'])
                    print('Nome do Serviço: ', conex_aux['servico'])
                    print('Conexão padrão? ', conex_aux['padrao'])
                
                print('='*50)


            elif escolha == 2:
                try:
                    print('='*50)
                    print('Nome da conexão: ', BD.nome_conexao_selecionada)
                    print('Usuário: ', BD.conexao_selecionada['usuario'])
                    print('IP do Banco: ', BD.conexao_selecionada['IP'])
                    print('Nome do Serviço: ', BD.conexao_selecionada['servico'])
                    print('Conexão padrão? ', BD.conexao_selecionada['padrao'])
                    print('='*50)
                except:
                    print('Sem conexão padrão selecionada!\nAdicione uma nova conexão ou escolha uma já existente.')


            elif escolha == 3:
                BD.adicionarConexao()

            
            elif escolha == 4: 
                nome_conexao = input('Escolha quais das coxeções você quer excluir: \n\t{}'.format(BD.conexoes.keys()))
                
                BD.removerConexao(nome_conexao)
                BD.selecionarConexaoPadrao()


            elif escolha == 0:
                break

    
    elif escolha == 3:
        with BD._conectarBanco() as dataBase:
            cur = dataBase.cursor()
            cur.execute("select status from v$instance")

            result = cur.fetone

            print(result)

    elif escolha == 4:
        BD.loadOracleClient()


    elif escolha == 0:
        break