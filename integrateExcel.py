# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:09:20 2016

@author: carlos

La función que realiza este script es la de leer el archivo csv que se nos pasa desde el CTI y 
lo guarda en la base de datos que tenemos creada en un mysql local de la máquina.

"""

import MySQLdb
import csv
import re



#select id_alu,assig,count(*),max(nota) as num_presentat from acta where presentat='S' and nota>5 group by id_alu,assig;

# Establecemos la conexin con la base de datos
bd = MySQLdb.connect("localhost","root","uib","epsdatamining" )

# Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
cursor = bd.cursor()

reader = csv.reader(open('datos.csv', 'rb'), delimiter=';')
for index,row in enumerate(reader):
	insertSentence="INSERT INTO acta (id_alu,pla,codi_ruct,assig,curs,tipus,credits,num_matric,any,convocatoria,presentat,mhonor,nota,qualificacio) VALUES ('"+row[0]+"','"+row[1]+"','"+row[3]+"','"+row[4]+"','"+row[5]+"','"+row[6]+"','"+row[7]+"','"+row[8]+"','"+row[9][:4]+"','"+row[10]+"','"+row[11]+"','"+row[12]+"','"+row[13].replace(",",".")+"','"+row[14]+"');"
	# Ejecutamos un query SQL usando el mtodo execute() que nos proporciona el cursor
	try:	
		cursor.execute(insertSentence)
		bd.commit()
	except:
		#print insertSentence
		bd.rollback


# Nos desconectamos de la base de datos
bd.close()
