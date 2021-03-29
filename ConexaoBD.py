import pickle
import cx_Oracle
import os
import glob
from time import sleep
from tkinter import filedialog, messagebox

class ConexaoBD():

    def __init__(self):
        self.dir_pad = os.getcwd()
        self.dirOraClient = self.loadOracleClient()
        self.conexoes = self.carregarConexoesSalvas()
        self.nome_conexao_selecionada = ''
        self.conexao_selecionada = self.pegarConexaoPadrao()
            

    def isConnectionsEmpty(self):
        return True if len(self.conexoes) == 0 else False


    def loadOracleClient(self):
        try:
            with open(os.path.join(self.dir_pad, "dirOracleClient.txt"), "r") as fileOracle:
                return fileOracle.read()
        except:
            try:
                if os.path.exists(os.path.join(self.dir_pad, glob.glob('instantclient*')[0])):
                    with open(os.path.join(self.dir_pad, "dirOracleClient.txt"), "w") as dirOracleClient:
                        dirOracleClient.write(os.path.join(self.dir_pad, glob.glob('instantclient*')[0]))
                    return os.path.join(self.dir_pad, glob.glob('instantclient*')[0])
            except:
                print("Não foi encontrada a pasta do Oracle Instant Client.\n"+
                        "Por favor, baixe a versão 32-bits dela em https://www.oracle.com/br/database/technologies/instant-client/downloads.html\n"+
                        "Depois indique onde ela está.")

                sleep(7)
                dirOracleClient = filedialog.askdirectory()
                with open(os.path.join(self.dir_pad, "dirOracleClient.txt"), "w") as dirOracle:
                    dirOracle.write(dirOracleClient)
                return dirOracleClient



    def initOracleClient(self):
        try:
            cx_Oracle.init_oracle_client(self.dirOraClient)
        except cx_Oracle.Error as erro:
            if str(erro) == "Oracle Client library has already been initialized":
                pass
            else:
                raise erro


    def quitcarregarConexoesSalvas(self):
        try:
            with open(os.path.join(self.dir_pad, "conexoes_salvas.dat"), 'rb') as dataFile:
                conexoes = pickle.load(dataFile)
            return conexoes
        
        except:
            conexao = self.createFirstConection()
            with open(os.path.join(self.dir_pad, "conexoes_salvas.dat"), 'wb') as dataFile:
                pickle.dump(conexao, dataFile)
            return conexao
    

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
        with open(os.path.join(self.dir_pad, 'conexoes_salvas.dat'), 'wb') as connection:
            pickle.dump(self.conexoes, connection)

    def removerConexao(self, nome_conexao):
        if self.isConnectionsEmpty():
            print("Você não tem conexões para remover!\nPor favor, insira uma:")
            self.createFirstConection()
        else:
            self.conexoes.pop(nome_conexao)
            with open(os.path.join(self.dir_pad, 'conexoes_salvas.dat'), 'wb') as connection:
                pickle.dump(self.conexoes, connection)
                self.selecionarConexaoPadrao()
            if self.isConnectionsEmpty():
                print("A conexão removida era a última!\nInsira uma nova:\n")
                self.createFirstConection()
                with open(os.path.join(self.dir_pad, 'conexoes_salvas.dat'), 'wb') as connection:
                    pickle.dump(self.conexoes, connection)



    def selecionarConexaoPadrao(self, conec_selecionada=None):
        try: 
            if conec_selecionada is None:
                conec_selecionada = input('Escolha uma dessas conexões para ser a padrão:\n\t{}'.format(self.conexoes.keys()))
            else:
                pass

            for conexao in self.conexoes:
                if self.conexoes[conexao]['padrao'] is True and conec_selecionada != conexao:
                    self.conexoes[conexao]['padrao'] = False
                else:
                    self.conexoes[conexao]['padrao'] = True
                    self.conexao_selecionada = self.pegarConexaoPadrao()
                    arq_dados = open(os.path.join(self.dir_pad, 'conexoes_salvas.dat'), 'wb')
                    pickle.dump(self.conexoes, arq_dados)
                    arq_dados.close()
                    

        except:
            print('Não existe nenhuma conexão com esse nome.')
            self.selecionarConexaoPadrao()


    def pegarConexaoPadrao(self):
        for conexao in self.conexoes:

            if self.conexoes[conexao]['padrao'] is True:
                self.nome_conexao_selecionada = conexao
                return self.conexoes[conexao]  

            else:
                 pass

    
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
            


