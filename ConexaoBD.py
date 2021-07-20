import cx_Oracle
from src.PersistenceManager import PersistenceManager

pm = PersistenceManager()

class ConexaoBD():

    def __init__(self):

        self.dirOraClient = pm.loadOracleClient()
        self.conexoes = pm.loadConections()
        self.nome_conexao_selecionada = ''
        self.conexao_selecionada = self.selectDefaultConection()
            

    def isConnectionsEmpty(self):
        return True if len(self.conexoes) == 0 else False

    
    def initOracleClient(self):
        try:
            cx_Oracle.init_oracle_client(self.dirOraClient)
        except cx_Oracle.Error as erro:
            if str(erro) == "Oracle Client library has already been initialized":
                pass
            else:
                raise erro
    

    def createFirstConection(self):
        nome_conexao = input('Digite o nome da Conexão: ')
        usuario = input('Digite o usuário de acesso ao Banco: ')
        senha = input('Digite a senha de acesso ao Banco: ')
        IP = input('Digite o IP onde está o Banco: ')
        servico = input('Digite o Nome do Serviço do Banco: ')
        

        conexao = {nome_conexao: {
                   'usuario': usuario,
                   'senha' : senha,
                   'IP' : IP,
                   'servico' : servico,
                   'padrao': True}}

        return conexao


    def createConection(self):
        nome_conexao = input('Digite o nome da Conexão: ')
        usuario = input('Digite o usuário de acesso ao Banco: ')
        senha = input('Digite a senha de acesso ao Banco: ')
        IP = input('Digite o IP onde está o Banco: ')
        servico = input('Digite o Nome do Serviço do Banco: ')
        

        while True:

            padrao = input('Essa conexão será a padrão? S/N\n')

            if padrao.lower() == 's':
                padrao = True
                break
            elif padrao.lower() == 'n':
                padrao = False
                break
            else:
                print('Digite apenas S ou N!')

        conexao = {nome_conexao: {
                   'usuario': usuario,
                   'senha' : senha,
                   'IP' : IP,
                   'servico' : servico,
                   'padrao': padrao}}


        return conexao
        

    def addConection(self):
        conection_registred = dict()
        
        if self.isConnectionsEmpty() is True:
            self.conexoes.update(self.createFirstConection())
            self.conexao_selecionada = self.selectDefaultConection()
        else:
            conection_registred = self.createConection()
            name_conection = list(conection_registred)[0]
            while name_conection in self.conexoes:
                name_conection = input('Já exite uma conexão com esse nome, por favor, escolha outro:\n>> ')
                conection_registred[name_conection]

            else:
                self.conexoes.update(conection_registred)
                
                if conection_registred[name_conection]['padrao'] is True:
                    self.ajustDefaultConections(name_conection)
                    self.conexao_selecionada = self.selectDefaultConection()
        
            pm.addConectionToFile(self.conexoes)
            return conection_registred


    def removerConexao(self, nome_conexao, isEmpty):
        if isEmpty:
            print("Você não tem conexões para remover!\nPor favor, insira uma:")
            nome_conexao = self.addConection()
            nome_conexao = list(nome_conexao)[0]
        else:

            if self.nome_conexao_selecionada == nome_conexao and nome_conexao in self.conexoes:
                removed_conection = self.conexoes.pop(nome_conexao)
                if self.isConnectionsEmpty():
                    pass
                else:
                    if len(self.conexoes) == 1:
                        self.ajustDefaultConections(list(self.conexoes)[0])
                        self.conexao_selecionada = self.selectDefaultConection()
                    else:
                        print('A conexão selecionada era a padrão, selecione uma nova:')
                        new_default_conection = input(f"{list(self.conexoes)}\n>>")
                        self.ajustDefaultConections(new_default_conection)
                        self.conexao_selecionada = self.selectDefaultConection()

            elif nome_conexao in self.conexoes:
                removed_conection = self.conexoes.pop(nome_conexao)

            elif nome_conexao not in self.conexoes:
                print("Conexão selecionada não existe, por favor insira uma existente.")
                return None

        if self.isConnectionsEmpty():
            print("conexão vazia no final")
            print("Você excluiu a última conexão. Insira uma nova: ")
            self.addConection()

        pm.addConectionToFile(self.conexoes)
        return removed_conection


    def ajustDefaultConections(self, conec_selecionada):
        for conexao in self.conexoes:
            if conec_selecionada == conexao:
                self.conexoes[conexao]['padrao'] = True
            else:
                self.conexoes[conexao]['padrao'] = False                 

    def selectDefaultConection(self):
        for conexao in self.conexoes:
            if self.conexoes[conexao]['padrao'] is True:
                self.nome_conexao_selecionada = conexao
                return self.conexoes[conexao]
        return None

    
    def conectarBanco(self):
        try:
            if self.conexao_selecionada is None:
                print("Não há conexão padrão. Crie uma nova para fazer a conexão com o banco.")
            else:
                self.initOracleClient()
                banco_conectado = cx_Oracle.connect(self.conexao_selecionada['usuario'] + '/' +
                                                    self.conexao_selecionada['senha'] + '@' +
                                                    self.conexao_selecionada['IP'] + '/' +
                                                    self.conexao_selecionada['servico'],
                                                    cclass = "HOL",
                                                    purity = cx_Oracle.ATTR_PURITY_SELF)

                print(f'Conexão com o Banco {self.nome_conexao_selecionada} realizada!')
                return banco_conectado
        except cx_Oracle.Error as erro:
            raise erro
            


