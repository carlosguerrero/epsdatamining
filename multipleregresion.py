# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:09:20 2016

@author: carlos

Crea los arboles de decision y prueba los archivos a ver como de eficaz es el método de clasificación
"""

def normalize(df):
#esta funcion traduce las notas numericas a simplemente indicar si ha aprobado p(pass) o suspendido f(fail)    
#    s = pd.Series(["np","f","f","f","f","f","p","p","p","p","p","p"],index=[-1,0,1,2,3,4,5,6,7,8,9,10])   
    s = pd.Series([0,1,1,1,1,1,2,2,2,2,2,2],index=[-1,0,1,2,3,4,5,6,7,8,9,10])   
    for index in df.keys():
        if index.endswith("nota"):
            df[index]=df[index].map(s)
    return df


def purgeColumns(df,tipo,asig):
    
    if (tipo=="all"):
        return df
    if (tipo=="nota"):
        indicesAborrar="presentados"
    if (tipo=="convocatorias"):
        indicesAborrar="nota"
    for index in df.keys():
        if (index.endswith(indicesAborrar) and (asig not in index)):
            df=df.drop(index,1)  
    return df


import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import ExperimentSetup

expsetup = ExperimentSetup.ExperimentSetup("geinPreExpedienteTodosExclusive2")
nombreDirectorio = "../csvFiles/"+expsetup.nombreExperimento+"/"
outfile=open('tressresults.txt','w')

import os
if os.path.exists('predictionResumen.csv'):
    os.remove('predictionResumen.csv')

resultStr = "Tipo" +";"+  "TipoDatos" +";"+ "Asignatura" +";"+ "Total" +";"+ "Aciertos" +";"+ "Suspendidos acertados" +";"+ "Suspendidos predichos" +";"+ "Suspensos totales" +";"+ "Ratio suspendidos" +";"+ "Ratio aciertos" +";"+ "Precision" +";"+ "Recall" +";"        
print(resultStr)

for tipo in ["all", "nota", "convocatorias"]:
#for tipo in ["convocatorias"]:
    if tipo=="all":
        starting_colum=3
    else:
        starting_colum=3
    
#    tipoDatos = "valornotas"
#    tipoDatos = "failpass"    

    for tipoDatos in ["valornotas", "failpass"]:


    
     #   for asigEstudio in expsetup.listadoAssigEstudio:
        for asigEstudio in ["21708"]:
            # Read in the csv file
        

        

    #        rowtrainingdataset = pd.read_csv(nombreDirectorio+str(asigEstudio)+tipo+".csv")
            rowtrainingdataset = pd.read_csv(nombreDirectorio+str(asigEstudio)+"all"+".csv")
            rowtrainingdataset = purgeColumns(rowtrainingdataset,tipo,str(asigEstudio)) 
            #la funcion purgeColumns lo que hace es quedarse solo con las columnas de tipo nota, o de tipo convocatoria o ambas
            #print(rowtrainingdataset)
            if (tipoDatos=="failpass"):
                trainingdataset = normalize(rowtrainingdataset)
                #la funcion normalize lo que hace es transformar las notas a aprobado o suspendido
            else:
                trainingdataset = rowtrainingdataset
            #print(trainingdataset)
            

            print(trainingdataset)
            #trainingsamples = trainingdataset.ix[:,starting_colum:]
            #classlabels_trainingsamples = trainingdataset.ix[:,starting_colum-1:starting_colum]
            #print(classlabels_trainingsamples)
            #print(trainingsamples)
            
            #clf = tree.DecisionTreeClassifier()
            #clf = clf.fit(trainingsamples,classlabels_trainingsamples)
            
            
            print(trainingdataset.describe()) 
            print(trainingdataset.corr())
            
           

