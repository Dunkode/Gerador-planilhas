import cx_Oracle
from src.PresistenceManager import PersistenceManager
pm = PersistenceManager()

class ConexaoBD():

    def __init__(self):

        self.dirOraClient = pm.loadOracleClient()
        self.conexoes = pm.loadConections()
        self.nome_conexao_selecionada = ''
        self.conexao_selecionada = self.pegarConexaoPadrao()
            

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
                   'padrao': 's'}}
        return conexao


    def criarConexao(self):
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

        self.selecionarConexaoPadrao(nome_conexao)
        
        return conexao
        

    def adicionarConexao(self):
        self.conexoes.update(self.criarConexao())
        pm.addConectionToFile(self.conexoes)

    def removerConexao(self, nome_conexao):
        if self.isConnectionsEmpty():
            print("Você não tem conexões para remover!\nPor favor, insira uma:")
            self.createFirstConection()
        else:
            self.conexoes.pop(nome_conexao)
            pm.addConectionToFile(self.conexoes)
            self.selecionarConexaoPadrao()
            if self.isConnectionsEmpty():
                print("A conexão removida era a última!\nInsira uma nova:\n")
                self.createFirstConection()
                pm.addConectionToFile(self.conexoes)


    def selecionarConexaoPadrao(self, conec_selecionada=None):
        try: 
            if conec_selecionada is None and not self.isConnectionsEmpty():
                conec_selecionada = input('Escolha uma dessas conexões para ser a padrão:\n\t{}\n>> '.format(self.conexoes.keys()))
            elif self.isConnectionsEmpty(): 
                print("Você não tem ennhuma conexão cadastrada!")
        except:
            print('Não existe nenhuma conexão com esse nome.')
            self.selecionarConexaoPadrao()

        for conexao in self.conexoes:
            if self.conexoes[conexao]['padrao'] is True or conec_selecionada != conexao:
                self.conexoes[conexao]['padrao'] = False
            else:
                self.conexoes[conexao]['padrao'] = True
            
        self.conexao_selecionada = self.pegarConexaoPadrao()
        pm.addConectionToFile(self.conexoes)
                    

        


    def pegarConexaoPadrao(self):
        for conexao in self.conexoes:
            if self.conexoes[conexao]['padrao'] is True:
                self.nome_conexao_selecionada = conexao
                return self.conexoes[conexao]  

    
    def conectarBanco(self):
        try:
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
            


