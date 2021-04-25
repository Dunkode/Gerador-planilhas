from xlwt import *
import xlwt
from time import sleep
from tkinter import filedialog
from os import mkdir, path, getcwd

class WorkbooktUtil():
    def __init__(self):
        self.saveDir = self.loadSaveDir()
    

    def askSaveDir(self):
        print("""Selecione o modo de escolha para o diretório onde serão salvas as planilhas geradas
              (1) Usar pasta onde está o programa
              (2) Escolher a pasta onde eles serão salvos.""")
        escolha = int(input())
        while True:
            if escolha == 1:
                with open(path.join(getcwd(), "dirSaveWorksheet.txt"), "w") as fileDir:
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


    def createWorkbook(self, dataToWrite, workbookName, columnNames):
        try:
            workbook = Workbook(encoding='UTF-8') 
            sheet = workbook.add_sheet("Sheet", cell_overwrite_ok= True)
            sheet = self.writeData(dataToWrite, sheet, columnNames)
            workbook.save(path.join(self.saveDir, workbookName+".xls"))

        except Exception as erro:
            raise erro

    def writeData(self, dataToWrite, sheetToWrite, columnNames):
        
        try:
            style = easyxf("font: bold on; align: wrap off, vert centre, horiz center")
            for column, name in enumerate(columnNames):
                sheetToWrite.write(0, column, label=name, style=style)

            for row, data in enumerate(dataToWrite):
                for column in range(len(data)):
                    sheetToWrite.write(row + 1, column, label=data[column])
            
            return sheetToWrite
        
        except Exception as erro:
            raise erro



