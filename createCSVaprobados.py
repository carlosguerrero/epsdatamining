#!/usr/bin/python

import MySQLdb



#select id_alu,assig,count(*),max(nota) as num_presentat from acta where presentat='S' and nota>5 group by id_alu,assig;

# Establecemos la conexin con la base de datos
bd = MySQLdb.connect("localhost","root","uib","epsdatamining" )

# Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cursorAlu = bd.cursor()
cursorAssig = bd.cursor()
cursorAluAssig = bd.cursor()

anyoEstudio =2014
asigEstudio =21708
asigCurso =2

#selectSentenceAlu="select distinct(id_alu) as codalu from acta where pla='gein' or pla='gin2' order by id_alu;"
#selectSentenceAssig="select distinct(assig) as codassig from acta where pla='gein' or pla='gin2' order by assig;"

#matrizAprobados debe de contener los expedientes de los alumnos una vez que habian aprobado la asignatura
#seleccionamos a todos aquellos alumnos que tienen la asigntarua aprobada antes del anyoEstudio y miramos el anyo en que aprobaron.
selectSentenceAlu="select id_alu,any from acta where (pla='gein' or pla='gin2') and any<"+str(anyoEstudio)+" and assig="+str(asigEstudio)+" and nota>5 order by id_alu;"
#seleccionamos las asginaturas de primero y segundo
selectSentenceAssig="select distinct(assig) as codassig from acta where (pla='gein' or pla='gin2') and curs<="+str(asigCurso)+" order by assig;"


try:
   # Ejecutamos el comando
   cursorAlu.execute(selectSentenceAlu)
   # Obtenemos todos los registros en una lista de listas
   resultadosAlu = cursorAlu.fetchall()
   matrizAprobados = {}
   for registroAlu in resultadosAlu:
	idalu=int(registroAlu[0])
	anyalu=int(registroAlu[1])
	matrizAprobados[idalu]={}
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
            matrizAprobados[idalu][str(idassig)+"presentados"]= registroAluAssig[0]
            #matrizAprobados[idalu][str(idassig)+"nota"]= registroAluAssig[1]
            #matrizAprobados[idalu][str(idassig)+"nota"]= registroAluAssig[1]
            #matrizAprobados[idalu][str(idassig)+"presentados"]= registroAluAssig[0]
	except:
	   print "Error: No se pudo obtener la data"
except:
   print "Error: No se pudo obtener la data"


print "matrizAprobados inicializada...."
print "Generando archivo de salida..."
outfile=open('csvAprobados.csv', 'w')
linea="idalumno"
for assigindex in matrizAprobados.itervalues().next().keys():
    linea+=","+str(assigindex)
#print(linea)
outfile.write(linea+"\n")
for aluindex in matrizAprobados.keys():
    linea=str(aluindex)
    for assigindex in matrizAprobados[aluindex].keys():
        linea += ","+str(matrizAprobados[aluindex][assigindex])
    #print(linea)
    outfile.write(linea+"\n")
outfile.close()
print "Archivo generado..."

#for aluenum, aluindex in enumerate(matrizAprobados):
#	linea=""
#	for asigenum,asigindex in enumerate(matrizAprobados[aluindex]):
#		linea = linea + ";" + str(asigindex)
#print "idalumno" + linea
#
#for aluenum, aluindex in enumerate(matrizAprobados):
#	linea=""
#	for asigenum,asigindex in enumerate(matrizAprobados[aluindex]):
#		linea = linea + ";" + str(matrizAprobados[aluindex][asigindex])
#	print str(aluindex) + linea


# Nos desconectamos de la base de datos
bd.close()
