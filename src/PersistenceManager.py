from os.path import join as pathAgregator
from os.path import exists
from os import getcwd, mkdir
from time import sleep
import glob
from tkinter import filedialog, messagebox
import pickle


class PersistenceManager:

    def __init__(self):
        self.dirDefault = getcwd()


    def loadOracleClient(self):
        try:
            with open(pathAgregator(self.dirDefault, "dirOracleClient.txt"), "r") as fileOracle:
                return fileOracle.read()
        except:
            try:
                dirOracleClient = pathAgregator(self.dirDefault, glob.glob('instantclient*')[0])
                if exists(dirOracleClient):
                    with open(pathAgregator(self.dirDefault, "dirOracleClient.txt"), "w") as dirOracleClientFile:
                        dirOracleClientFile.write(dirOracleClient)
                    return dirOracleClient
            except:
                print("Não foi encontrada a pasta do Oracle Instant Client.\n"+
                        "Por favor, baixe a versão 32-bits dela em https://www.oracle.com/br/database/technologies/instant-client/downloads.html\n"+
                        "Depois indique onde ela está.")

                sleep(7)
                dirOracleClient = filedialog.askdirectory()
                with open(pathAgregator(self.dirDefault, "dirOracleClient.txt"), "w") as dirOracle:
                    dirOracle.write(dirOracleClient)
                return dirOracleClient


    def loadConections(self):
        with open(pathAgregator(self.dirDefault, "conexoes_salvas.dat"), 'rb') as dataFile:
            conexoes = pickle.load(dataFile)
        return conexoes
        
    def addConectionToFile(self, conection):
        with open(pathAgregator(self.dirDefault, "conexoes_salvas.dat"), 'wb') as dataFile:
            pickle.dump(conection, dataFile)
        return conection


    def askSaveDirWorkbooks(self):
        print("""Selecione o modo de escolha para o diretório onde serão salvas as planilhas geradas
              (1) Usar pasta onde está o programa
              (2) Escolher a pasta onde eles serão salvos.""")
        escolha = int(input())
        while True:
            if escolha == 1:
                with open(pathAgregator(self.dirDefault, "dirSaveWorksheet.txt"), "w") as dirFile:
                    dirWay = pathAgregator(self.dirDefault, "SavedWorksheets") 
                    mkdir(dirWay)
                    dirFile.write(dirWay)
                    return dirWay

            elif escolha == 2:
                print("Selecione o diretório onde você vai querer salvar as planilhas")
                sleep(3)
                with open(pathAgregator(self.dirDefault, "dirSaveWorksheet.txt"), "w") as dirFile:
                    dirSelected = filedialog.askdirectory()
                    dirFile.write(dirSelected)
                    return dirSelected 

    def loadSaveDirWorkbooks(self):
        try:
            with open(pathAgregator(self.dirDefault, "dirSaveWorksheet.txt"), "r") as dirFile:
                return dirFile.read()
        except:
            return self.askSaveDirWorkbooks()