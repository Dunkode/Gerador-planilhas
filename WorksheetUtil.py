from xlwt import *
from time import sleep
from tkinter import filedialog
from os import *

class WorksheetUtil():
    def __init__(self):
        self.saveDir = self.loadSaveDir()
    

    def askSaveDir(self):
        print("""Selecione o modo de escolha para o diretório onde serão salvas as planilhas geradas
              (1) Usar pasta onde está o programa
              (2) Escolher a pasta onde eles serão salvos.""")
        escolha = int(input())
        while True:
            if escolha == 1:
                with open(path.join(getcwd(), "dirSaveWorksheet.txt", "w")) as fileDir:
                    dirWay = path.join(getcwd(), "SavedWorksheets") 
                    mkdir(dirWay)
                    fileDir.write(dirWay)
                    return dirWay

            elif escolha == 2:
                print("Selecione o diretório onde você vai querer salvar as planilhas")
                sleep(3)
                with open(path.join(getcwd(), "dirSaveWorksheet.txt"), "w") as fileDir:
                    fileDir.write(filedialog.askdirectory())
                    return filedialog.askdirectory()

    def loadSaveDir(self):
        try:
            with open(path.join(getcwd(), "dirSaveWorksheet.txt"), "r") as fileDir:
                return fileDir.read()
        except:
            return self.askSaveDir()


    def createWorksheet(self, dataToWrite, tableName, workbookName):
        workbook = Workbook(encoding='UTF-8')
        try:
            sheet = workbook.add_sheet("Sheet", cell_overwirte_ok= True)
        except :
            print("Falha ao gerar planilha...")