#!/usr/bin/python

import MySQLdb



#select id_alu,assig,count(*),max(nota) as num_presentat from acta where presentat='S' and nota>5 group by id_alu,assig;

# Establecemos la conexin con la base de datos
bd = MySQLdb.connect("localhost","root","uib","epsdatamining" )

# Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cursorAlu = bd.cursor()
cursorAssig = bd.cursor()

selectSentenceAlu="select distinct(id_alu) as codalu from acta where pla='gein' or pla='gin2' order by id_alu;"
selectSentenceAssig="select distinct(assig) as codassig from acta where pla='gein' or pla='gin2' order by assig;"


try:
   # Ejecutamos el comando
   cursorAlu.execute(selectSentenceAlu)
   # Obtenemos todos los registros en una lista de listas
   resultadosAlu = cursorAlu.fetchall()
   matriz = {}
   for registroAlu in resultadosAlu:
	idalu=int(registroAlu[0])
	matriz[idalu]={}
	try:
	   # Ejecutamos el comando
	   cursorAssig.execute(selectSentenceAssig)
	   # Obtenemos todos los registros en una lista de listas
	   resultadosAssig = cursorAssig.fetchall()
	   for registroAssig in resultadosAssig:
	      matriz[idalu][int(registroAssig[0])]=0
	except:
	   print "Error: No se pudo obtener la data"
except:
   print "Error: No se pudo obtener la data"

anyoEstudio =2014
asigEstudio =21724
print "Matriz inicializada...."
cursorActa = bd.cursor()
#selectSentenceActa="select id_alu,assig,count(*) as num_presentat,max(nota) as nota from acta where presentat='S' and (pla='gein' or pla='gin2') group by id_alu,assig;"
#el anyo tiene que ser menor estricto ya que el eestudio del año actual se hace con el de las notas el año anterior.
selectSentenceActa="select id_alu,assig,count(*) as num_presentat,max(nota) as nota from acta where id_alu IN (SELECT id_alu,any,assig,nota where any<"+str(anyoEstudio)+" and assig="+str(asigEstudio)+") and presentat='S' and (pla='gein' or pla='gin2') and any<"+ str(anyoEstudio)+" group by id_alu,assig;"
try:
   # Ejecutamos el comando
   cursorActa.execute(selectSentenceActa)
   # Obtenemos todos los registros en una lista de listas
   resultadosActa = cursorActa.fetchall()
   for registroActa in resultadosActa:
      matriz[int(registroActa[0])][int(registroActa[1])]=float(registroActa[3])
      #matriz[int(registroActa[0])][int(registroActa[1])]=4
except:
   print "Error: No se pudo obtener la data"

for aluenum, aluindex in enumerate(matriz):
	linea=""
	for asigenum,asigindex in enumerate(matriz[aluindex]):
		linea = linea + ";" + str(asigindex)
print "idalumno" + linea

for aluenum, aluindex in enumerate(matriz):
	linea=""
	for asigenum,asigindex in enumerate(matriz[aluindex]):
		linea = linea + ";" + str(matriz[aluindex][asigindex])
	print str(aluindex) + linea


# Nos desconectamos de la base de datos
bd.close()
