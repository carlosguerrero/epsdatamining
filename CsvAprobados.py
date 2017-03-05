#!/usr/bin/python

class CsvAprobados:


    


    anyoEstudio = 0;
    asigEstudio = 0;
    asigCurso = 0;
    
    





    def __init__(self, anyo, assignatura, curso):
        self.anyoEstudio = anyo
        self.asigEstudio = assignatura
        self.asigCurso = curso
        self.matrizAprobados = {}
        
    def generarMatriz(self):

        import MySQLdb        
        
        #matrizAprobados debe de contener los expedientes de los alumnos una vez que habian aprobado la asignatura
         
        # Establecemos la conexin con la base de datos
        bd = MySQLdb.connect("localhost","root","uib","epsdatamining" )
        # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
        cursorAlu = bd.cursor()
        cursorAssig = bd.cursor()
        cursorAluAssig = bd.cursor()   
        #seleccionamos a todos aquellos alumnos que tienen la asigntarua aprobada antes del anyoEstudio y miramos el anyo en que aprobaron.
        selectSentenceAlu="select id_alu,any from acta where (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig="+str(self.asigEstudio)+" and nota>5 order by id_alu;"
        #seleccionamos las asginaturas de primero y segundo
        selectSentenceAssig="select distinct(assig) as codassig from acta where (pla='gein' or pla='gin2') and curs<="+str(self.asigCurso)+" order by assig;"
        try:
           # Ejecutamos el comando
           cursorAlu.execute(selectSentenceAlu)
           # Obtenemos todos los registros en una lista de listas
           resultadosAlu = cursorAlu.fetchall()
           
           for registroAlu in resultadosAlu:
               idalu=int(registroAlu[0])
               anyalu=int(registroAlu[1])
               self.matrizAprobados[idalu]={}
               try:
                   # Ejecutamos el comando
                   cursorAssig.execute(selectSentenceAssig)
                   # Obtenemos todos los registros en una lista de listas
                   resultadosAssig = cursorAssig.fetchall()
                   for registroAssig in resultadosAssig:
                       idassig=int(registroAssig[0])
                       selectSenteceAluAssig = "select count(*) as num_presentat,max(nota) as nota from acta where assig="+str(idassig)+" and id_alu="+str(idalu)+" and any<="+str(anyalu)+";"
                       cursorAluAssig.execute(selectSenteceAluAssig)
                       registroAluAssig = cursorAluAssig.fetchone()
                       self.matrizAprobados[idalu][str(idassig)+"presentados"]= registroAluAssig[0]
                       if (str(registroAluAssig[1]) != "None"):
                           self.matrizAprobados[idalu][str(idassig)+"nota"]= int(registroAluAssig[1])
                       else:
                           self.matrizAprobados[idalu][str(idassig)+"nota"]= "-1"
                       
               except:
                   print "Error: No se pudo obtener la data("+registroAluAssig[1]+")"
        except:
           print "Error: No se pudo obtener la data"
    
        print "matrizAprobados inicializada...."
        bd.close()
        
        
    def escribirCsv(self):
        print "Generando archivo de "+str(self.asigEstudio)+"..."
        outfileA=open(str(self.asigEstudio)+'all.csv', 'w')
        outfileC=open(str(self.asigEstudio)+'convocatorias.csv', 'w')
        outfileN=open(str(self.asigEstudio)+'nota.csv', 'w')
        lineaA="idalumno"        
        lineaC="idalumno"
        lineaN="idalumno"
        for assigindex in self.matrizAprobados.itervalues().next().keys():
            lineaA+=","+str(assigindex)
        outfileA.write(lineaA+"\n")
        outfileC.write(lineaC+"\n")
        outfileN.write(lineaN+"\n")
        for aluindex in self.matrizAprobados.keys():
            lineaA=str(aluindex)
            lineaC=str(aluindex)
            lineaN=str(aluindex)
            for assigindex in self.matrizAprobados[aluindex].keys():
                try:
                    lineaA += ","+str(self.matrizAprobados[aluindex][assigindex])
                except:
                    print "valor incorrecto("+self.matrizAprobados[aluindex][assigindex]+")"
            outfileA.write(lineaA+"\n")
            outfileC.write(lineaC+"\n")
            outfileN.write(lineaN+"\n")
        outfileA.close()
        outfileC.close()
        outfileN.close()
        print "Archivo generado..."
    
    # Nos desconectamos de la base de datos

