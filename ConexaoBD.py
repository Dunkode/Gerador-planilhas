import cx_Oracle
from src.PersistenceManager import PersistenceManager

pm = PersistenceManager()

class ConexaoBD():

    def __init__(self):

        self.__dirOraClient = pm.loadOracleClient()
        self.conexoes = pm.loadConections()
        self.conexao_selecionada = self.__selectDefaultConection()
            

    def __isConnectionsEmpty(self):
        return True if len(self.conexoes) == 0 else False

    
    def __initOracleClient(self):
        try:
            cx_Oracle.init_oracle_client(self.__dirOraClient)
        except cx_Oracle.Error as erro:
            if str(erro) == "Oracle Client library has already been initialized":
                pass
            else:
                raise erro
    

    def __createFirstConection(self):
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


    def __createConection(self):
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
        
        if self.__isConnectionsEmpty() is True:
            self.conexoes.update(self.__createFirstConection())
            self.conexao_selecionada = self.__selectDefaultConection()
        else:
            conection_registred = self.__createConection()
            name_conection = list(conection_registred)[0]
            
            while name_conection in self.conexoes:
                old_conection = conection_registred[name_conection]
                name_conection = input('Já exite uma conexão com esse nome. Por favor, escolha outro:\n>> ')
                conection_registred = {name_conection : old_conection}

            self.conexoes.update(conection_registred)
                
            if conection_registred[name_conection]['padrao'] is True:
                self.__ajustDefaultConections(name_conection)
                self.conexao_selecionada = self.__selectDefaultConection()
        
            pm.addConectionToFile(self.conexoes)
            return conection_registred
    

    def __removeConection(self, nome_conexao):
        if nome_conexao is None:
            print("Você não tem conexões para remover!\nPor favor, insira uma:")
            nome_conexao = self.addConection()
            return None
        else:
            if nome_conexao in self.conexoes:
                removed_conection = self.conexoes.pop(nome_conexao)  

                if self.__isConnectionsEmpty():
                    print("Você excluiu a última conexão. Insira uma nova: ")
                    self.addConection()
                    return None
                
                elif self.conexao_selecionada == nome_conexao:
                        if len(self.conexoes) == 1:
                            self.__ajustDefaultConections(list(self.conexoes)[0])
                            self.conexao_selecionada = self.__selectDefaultConection()
                        else:
                            print('A conexão selecionada era a padrão, selecione uma nova:')
                            new_default_conection = input(f"{list(self.conexoes)}\n>>")
                            self.__ajustDefaultConections(new_default_conection)
                            self.conexao_selecionada = self.__selectDefaultConection()
                        
            else:
                print("Conexão selecionada não existe, por favor insira uma existente.")
                return None

        pm.addConectionToFile(self.conexoes)
        return removed_conection

    def popConection(self):
        if self.__isConnectionsEmpty() is True:
           self.__removeConection(None)
        else:
            nome_conexao = input('Escolha quais das coxeções você quer excluir: \n\t{}'.format(self.conexoes.keys()))
            self.__removeConection(nome_conexao)


    def __ajustDefaultConections(self, conec_selecionada):
        for conexao in self.conexoes:
            if conec_selecionada == conexao:
                self.conexoes[conexao]['padrao'] = True
            else:
                self.conexoes[conexao]['padrao'] = False                 

    def __selectDefaultConection(self):
        for conexao in self.conexoes:
            if self.conexoes[conexao]['padrao'] is True:
                return conexao
        return None


    def editConection(self):
        print(f"Selecione uma das conexões para ser editada: \n{self.conexoes.keys()}")
        conection_edit = input('\n>> ')
        field = ''

        while conection_edit not in self.conexoes:
            print(f"A conexão digitada não existe, escolha uma dessas: \n{self.conexoes.keys()}")
            conection_edit = input('\n>> ')

        while True:
            print("Escolha qual das informações você quer alterar:\n"
                    "(1) Usuario\n"+
                    "(2) Senha\n"+
                    "(3) IP e Porta\n"+
                    "(4) Nome do Serviço\n" +
                    f"(0) Sair sair das alterações na conexão {conection_edit}")
            escolha = int(input("\n>> "))

            if escolha == 1:
                field = 'usuario'
            elif escolha == 2:
                field = 'senha'
            elif escolha == 3:
                field = 'IP'
            elif escolha == 4:
                field = 'servico'
            elif escolha == 0:
                break
            else:
                print("Digite um valor válido!")
                continue
            
            print("Digite o novo valor: ")
            new_value = input("\n>> ")
            
            if escolha != 2:
                old_value = self.conexoes[conection_edit][field]
                self.conexoes[conection_edit][field] = new_value
                print(f"\nCampo {field} alterado de {old_value} para {new_value} com sucesso!\n")
            else: 
                print(f"\nSenha de {conection_edit} alterada com sucesso!\n")
        
        pm.addConectionToFile(self.conexoes)

    
    def conectarBanco(self):
        try:
            if self.conexao_selecionada is None:
                print("Não há conexão padrão. Crie uma nova para fazer a conexão com o banco.")
            else:
                self.__initOracleClient()
                print(self.conexoes[self.conexao_selecionada])
                banco_conectado = cx_Oracle.connect(self.conexoes[self.conexao_selecionada]['usuario'] + '/' +
                                                    self.conexoes[self.conexao_selecionada]['senha'] + '@' +
                                                    self.conexoes[self.conexao_selecionada]['IP'] + '/' +
                                                    self.conexoes[self.conexao_selecionada]['servico'],
                                                    cclass = "HOL",
                                                    purity = cx_Oracle.ATTR_PURITY_SELF)

                print(f'Conexão com o Banco {self.conexao_selecionada} realizada!')
                return banco_conectado
        except cx_Oracle.Error as erro:
            raise erro
            


