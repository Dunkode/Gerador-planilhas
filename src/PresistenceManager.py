from os.path import join as pathAgregator
from os.path import exists
from os import getcwd
from time import sleep
import glob
from tkinter import filedialog, messagebox
import pickle


class PersistenceManager:

    def __init__(self):
        self.dir_pad = getcwd()


    def loadOracleClient(self):
        try:
            with open(pathAgregator(self.dir_pad, "dirOracleClient.txt"), "r") as fileOracle:
                return fileOracle.read()
        except:
            try:
                dirOracleClient = pathAgregator(self.dir_pad, glob.glob('instantclient*')[0])
                if exists(dirOracleClient):
                    with open(pathAgregator(self.dir_pad, "dirOracleClient.txt"), "w") as dirOracleClientFile:
                        dirOracleClientFile.write(dirOracleClient)
                    return dirOracleClient
            except:
                print("Não foi encontrada a pasta do Oracle Instant Client.\n"+
                        "Por favor, baixe a versão 32-bits dela em https://www.oracle.com/br/database/technologies/instant-client/downloads.html\n"+
                        "Depois indique onde ela está.")

                sleep(7)
                dirOracleClient = filedialog.askdirectory()
                with open(pathAgregator(self.dir_pad, "dirOracleClient.txt"), "w") as dirOracle:
                    dirOracle.write(dirOracleClient)
                return dirOracleClient

    def loadConections(self):
        with open(pathAgregator(self.dir_pad, "conexoes_salvas.dat"), 'rb') as dataFile:
            conexoes = pickle.load(dataFile)
        return conexoes
        
    def addConectionToFile(self, conection):
        with open(pathAgregator(self.dir_pad, "conexoes_salvas.dat"), 'wb') as dataFile:
            pickle.dump(conection, dataFile)
        return conection