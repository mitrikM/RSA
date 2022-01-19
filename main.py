import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHeaderView, QTableWidgetItem,QVBoxLayout
from PyQt5 import QtGui, uic, QtCore

import sympy
import random
import math 
#import unidecode 

qtCreatorFile = "kryptoUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    return (str1.join(s))
class MyApp(QMainWindow, Ui_MainWindow):
    def getKeys(self):
        minNum= 10000000000
        maxNum= 99999999999
        p = sympy.randprime(minNum,maxNum)
        q= sympy.randprime(minNum,maxNum)
        
        while p==q:
            q= sympy.randprime(minNum,maxNum)
            
        n=p*q
        
        totient= (p-1)*(q-1)
        
        e= random.randint(1, n)
        
        while math.gcd(e,totient) !=1:
            e= random.randint(1, n)
        
        d= pow(e,-1,totient)
        privateKey=[d,n]
        publicKey=[e,n]
        
        self.labelVysledek_2.setText("public key = " + str(publicKey) + "\nprivate key = " + str(privateKey))
        if self.CheckBox_Sifrovat.isChecked():
            self.hodnotaA.setPlainText(str(n))
            self.hodnotaA_2.setPlainText(str(e))
        elif self.CheckBox_Desifrovat.isChecked():
            self.hodnotaA.setPlainText(str(n))
            self.hodnotaA_2.setPlainText(str(d))
        
        
    def encrypt(self):


        plainText=str(self.plainTextEdit_Input.toPlainText()) 
        i=0
        cypherText=[]
        while(i<len(plainText)):
            BigNumber=""
            binaryText=[]
            if i+6 > len(plainText):
                maxIndex=len(plainText)
            else:
                maxIndex=i+6
            for j in range (i,maxIndex):
                num=ord(plainText[j])
                binaryText.append(f'{num:012b}') 
            for j in range(0,maxIndex-i):
                BigNumber+=binaryText[j]
                
            BigNumber=int(BigNumber,2)
            x=pow(BigNumber,int(self.hodnotaA_2.toPlainText()),int(self.hodnotaA.toPlainText()))
            cypherText.append(x)
            i+=6
        cypherText= str(cypherText)
        cypherText=listToString(cypherText)
        cypherText= cypherText.replace("'","")
        cypherText=cypherText.replace(",","")
        cypherText=cypherText.replace("[","")
        cypherText=cypherText.replace("]","")
        self.labelVysledek.setText(cypherText)

    
    def decrypt(self):
        d=int(self.hodnotaA_2.toPlainText())
        n=int(self.hodnotaA.toPlainText())

        vstup=str(self.plainTextEdit_Input.toPlainText()) 

        i=0
        bigNumber=""
        x=[]
        while i<len(vstup):
            
            

            if not(vstup[i]==" " or i==len(vstup)-1):

                bigNumber+=vstup[i]


            else:
                if i==len(vstup)-1:
                    bigNumber+=vstup[i]

            
                bigNumber=pow(int(bigNumber),d,n)
                binNum=format(bigNumber,'b')
                if len(binNum)%12!=0:
                    for p in range(12-len(binNum)%12):
                        binNum=''.join(('0',binNum))
                        
                j=0 
                while  j<len(binNum):
                    blok=[]
                    for k in range(j,j+12):
                        blok.append(binNum[k])
                    blok=listToString(blok)
                    blok=int(blok,2)
                    pom=chr(blok)
                    pom=str(pom)
                    x.append((pom))
                    j+=12
                    bigNumber=""

                    
                    



            i+=1 

        vysledok=""
        for i in range(0,len(x)):
            vysledok+=x[i]
        self.labelVysledek.setText(vysledok)

        
       

            
            

    def execute(self):
        if self.CheckBox_Desifrovat.isChecked():
            self.decrypt()
        elif self.CheckBox_Sifrovat.isChecked():
            self.encrypt()

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Button_Execute.clicked.connect(self.execute)  
        self.pushButton.clicked.connect(self.getKeys)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())        
           
        
    
    
