#!/usr/bin/python

class CsvExpediente:


    def __init__(self, expsetup):
        self.expSetup = expsetup
        self.matrizHistoricos = {}
        self.matrizActuales = {}


    def inicializarMatriz(self,resultadosAlu,resultadosAssig,matriz,bd):
        for registroAlu in resultadosAlu:
            idalu=int(registroAlu[0])
            anyclavealu=int(registroAlu[2])
            matriz[str(idalu)+"-"+str(anyclavealu)]={}
            try:
                for registroAssig in resultadosAssig:
                    idassig=int(registroAssig[0])
                    matriz[str(idalu)+"-"+str(anyclavealu)][str(idassig)+"presentados"]= 0
                    matriz[str(idalu)+"-"+str(anyclavealu)][str(idassig)+"nota"]= "-1"
                       
            except:
                print "Error: No se pudo obtener la data"        
        
    def anyadirAMatriz(self,resultadosAlu,resultadosAssig,matriz,bd):
        cursorAluAssig = bd.cursor()
        for registroAlu in resultadosAlu:
            idalu=int(registroAlu[0])
            anyalu=int(registroAlu[1])
            anyclavealu=int(registroAlu[2])
            #self.matrizHistoricos[idalu]={}
            try:
                for registroAssig in resultadosAssig:
                    idassig=int(registroAssig[0])
                    selectSenteceAluAssig = "select count(*) as num_presentat,max(nota) as nota from acta where assig="+str(idassig)+" and id_alu="+str(idalu)+" and any<="+str(anyalu)+";"
                    cursorAluAssig.execute(selectSenteceAluAssig)
                    registroAluAssig = cursorAluAssig.fetchone()
                    matriz[str(idalu)+"-"+str(anyclavealu)][str(idassig)+"presentados"]= registroAluAssig[0]
                    if (str(registroAluAssig[1]) != "None"):
                        matriz[str(idalu)+"-"+str(anyclavealu)][str(idassig)+"nota"]= int(float(round(registroAluAssig[1],0)))
                    else:
                        matriz[str(idalu)+"-"+str(anyclavealu)][str(idassig)+"nota"]= "-1"
                       
            except:
                print "Error: No se pudo obtener la data("+registroAluAssig[1]+")"

    
    def generarMatriz(self):

        import MySQLdb
        import sys

        
        #matrizHistoricos debe de contener los expedientes de los alumnos una vez que habian aprobado la asignatura
         
        # Establecemos la conexin con la base de datos
        bd = MySQLdb.connect("localhost","root","uib","epsdatamining" )
        # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
        cursorAlu = bd.cursor()
        cursorAssig = bd.cursor()
           
        try:
           #Inicializarmos la matriz todo a valor por defecto
           # Ejecutamos el comando
           print(self.expSetup.getSelectSentenceAllAlu())
           cursorAlu.execute(self.expSetup.getSelectSentenceAllAlu())
           # Obtenemos todos los registros en una lista de listas
           rsAlu = cursorAlu.fetchall()
           print(self.expSetup.getSelectSentenceAllAssig())
           cursorAssig.execute(self.expSetup.getSelectSentenceAllAssig())
           rsAssig = cursorAssig.fetchall()
           self.inicializarMatriz(rsAlu,rsAssig,self.matrizHistoricos,bd)
           
           #Introducimos la informacion de los expedientes de los alumnos aprobados
           print(self.expSetup.getSelectSentenceAnyoPrevioAluAprob())
           cursorAlu.execute(self.expSetup.getSelectSentenceAnyoPrevioAluAprob())
           rsAlu = cursorAlu.fetchall()
           print(self.expSetup.getSelectSentenceAssigExpedienteAlu())
           cursorAssig.execute(self.expSetup.getSelectSentenceAssigExpedienteAlu())
           rsAssig = cursorAssig.fetchall()           
           self.anyadirAMatriz(rsAlu,rsAssig,self.matrizHistoricos,bd)
           
           #Introducimos la informacion de la asignatura a estudiar
           print(self.expSetup.getSelectSentenceAnyoAprobAlu())
           cursorAlu.execute(self.expSetup.getSelectSentenceAnyoAprobAlu())
           rsAlu = cursorAlu.fetchall()
           print(self.expSetup.getSelectSentenceAssigPredecir())
           cursorAssig.execute(self.expSetup.getSelectSentenceAssigPredecir())
           rsAssig = cursorAssig.fetchall()           
           self.anyadirAMatriz(rsAlu,rsAssig,self.matrizHistoricos,bd)
           
           
           
           
           ### Pasamos a crear la matriz para los alumnosq ue la cursan actualmente
           
           
           
           
           
           
           #Inicializarmos la matriz todo a valor por defecto
           # Ejecutamos el comando
           print(self.expSetup.getSelectSentenceAllAluActual())
           cursorAlu.execute(self.expSetup.getSelectSentenceAllAluActual())
           # Obtenemos todos los registros en una lista de listas
           rsAlu = cursorAlu.fetchall()
           print(self.expSetup.getSelectSentenceAllAssig())
           cursorAssig.execute(self.expSetup.getSelectSentenceAllAssig())
           rsAssig = cursorAssig.fetchall()
           self.inicializarMatriz(rsAlu,rsAssig,self.matrizActuales,bd)
           
           #Introducimos la informacion de los expedientes del curso anterior
           print(self.expSetup.getSelectSentenceAnyoPrevioAluActual())
           cursorAlu.execute(self.expSetup.getSelectSentenceAnyoPrevioAluActual())
           rsAlu = cursorAlu.fetchall()
           print(self.expSetup.getSelectSentenceAssigExpedienteAlu())
           cursorAssig.execute(self.expSetup.getSelectSentenceAssigExpedienteAlu())
           rsAssig = cursorAssig.fetchall()           
           self.anyadirAMatriz(rsAlu,rsAssig,self.matrizActuales,bd)
           
           #Introducimos la informacion de la asignatura a estudiar
           print(self.expSetup.getSelectSentenceAnyoActualAluActual())
           cursorAlu.execute(self.expSetup.getSelectSentenceAnyoActualAluActual())
           rsAlu = cursorAlu.fetchall()
           print(self.expSetup.getSelectSentenceAssigPredecir())
           cursorAssig.execute(self.expSetup.getSelectSentenceAssigPredecir())
           rsAssig = cursorAssig.fetchall()           
           self.anyadirAMatriz(rsAlu,rsAssig,self.matrizActuales,bd)
           
        except:
           print "Error: No se pudo obtener la dataaaa"
           print("Unexpected error:", sys.exc_info()[0])
    
        print "matrizHistoricos inicializada...."
        bd.close()
        
        
    def escribirCsv(self):
        self.escribirCsvGeneric(self.matrizHistoricos,"")
        self.escribirCsvGeneric(self.matrizActuales,"C")
        
        
        
    def escribirCsvGeneric(self,matriz,filename):
        
        import os        
        
        print "Generando archivo de "+str(self.expSetup.asigEstudio)+"..."
        nombreDirectorio = "../csvFiles/"+self.expSetup.nombreExperimento+"/"
        if not os.path.exists(nombreDirectorio): os.makedirs(nombreDirectorio)
        outfileA=open(nombreDirectorio+str(self.expSetup.asigEstudio)+filename+'all.csv', 'w')
        outfileC=open(nombreDirectorio+str(self.expSetup.asigEstudio)+filename+'convocatorias.csv', 'w')
        outfileN=open(nombreDirectorio+str(self.expSetup.asigEstudio)+filename+'nota.csv', 'w')
        lineaA="idalumno,"+str(self.expSetup.asigEstudio)+"presentados,"+str(self.expSetup.asigEstudio)+"nota"       
        lineaC="idalumno,"+str(self.expSetup.asigEstudio)+"presentados"
        lineaN="idalumno,"+str(self.expSetup.asigEstudio)+"nota"
        for assigindex in matriz.itervalues().next().keys():
            if str(self.expSetup.asigEstudio) not in assigindex:
                lineaA+=","+str(assigindex)
                if ("presentados" in assigindex):
                    lineaC +=","+str(assigindex)
                if ("nota" in assigindex):
                    lineaN +=","+str(assigindex)           

        outfileA.write(lineaA+"\n")
        outfileC.write(lineaC+"\n")
        outfileN.write(lineaN+"\n")
        for aluindex in matriz.keys():
            lineaA=str(aluindex)+","+str(matriz[aluindex][str(self.expSetup.asigEstudio)+"presentados"])+","+str(matriz[aluindex][str(self.expSetup.asigEstudio)+"nota"])
            lineaC=str(aluindex)+","+str(matriz[aluindex][str(self.expSetup.asigEstudio)+"presentados"])
            lineaN=str(aluindex)+","+str(matriz[aluindex][str(self.expSetup.asigEstudio)+"nota"])
            for assigindex in matriz[aluindex].keys():
                try:
                    if str(self.expSetup.asigEstudio) not in assigindex:
                        lineaA += ","+str(matriz[aluindex][assigindex])
                        if "presentados" in str(assigindex):
                            lineaC += ","+str(matriz[aluindex][assigindex])
                        if "nota" in str(assigindex):
                            lineaN += ","+str(matriz[aluindex][assigindex])           
                except:
                    print "valor incorrecto("+matriz[aluindex][assigindex]+")"
            outfileA.write(lineaA+"\n")
            outfileC.write(lineaC+"\n")
            outfileN.write(lineaN+"\n")
        outfileA.close()
        outfileC.close()
        outfileN.close()
        print "Archivo generado..."
    
    # Nos desconectamos de la base de datos

