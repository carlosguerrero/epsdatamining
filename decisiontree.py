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

        total = 0;
        totalaciertos = 0;
        totalsuspaciertos = 0;
        totalsusppredict = 0;
        totalsusp = 0;
    
        for asigEstudio in expsetup.listadoAssigEstudio:
    #    for asigEstudio in ["21708"]:
            # Read in the csv file
        
            asig_total = 0;
            asig_totalaciertos = 0;
            asig_totalsuspaciertos = 0;
            asig_totalsusppredict = 0;
            asig_totalsusp = 0;
    
        
            outfile.write("#####"+str(asigEstudio)+"\n")
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
            
            
            
            trainingsamples = trainingdataset.ix[:,starting_colum:]
            classlabels_trainingsamples = trainingdataset.ix[:,starting_colum-1:starting_colum]
            #print(classlabels_trainingsamples)
            #print(trainingsamples)
            
            #clf = tree.DecisionTreeClassifier()
            #clf = clf.fit(trainingsamples,classlabels_trainingsamples)
            
            
            clf = RandomForestClassifier()        
            clf = clf.fit(trainingsamples,classlabels_trainingsamples.values.ravel())
            
            #print(clf)
            
    #        with open("iris.dot", 'w') as f:
    #            f = tree.export_graphviz(clf, out_file=f)
                
            rowtoclassifydataset = pd.read_csv(nombreDirectorio+str(asigEstudio)+"C"+"all"+".csv")
            rowtoclassifydataset = purgeColumns(rowtoclassifydataset,tipo,str(asigEstudio))
            #print(rowtoclassifydataset)
            if (tipoDatos=="failpass"):
                toclassifydataset = normalize(rowtoclassifydataset)
            else:
                toclassifydataset = rowtoclassifydataset
            samples = toclassifydataset.ix[:,starting_colum:].as_matrix()
            correctclass = toclassifydataset.ix[:,starting_colum-1:starting_colum]
            
            evaluation = toclassifydataset.ix[:,starting_colum-1:]
            
    
            
            for i,row in evaluation.iterrows():
                real=row[0]
                predict=clf.predict(toclassifydataset.ix[i][starting_colum:].reshape(1,-1))
                outfile.write(str(real)+str(predict)+"\n")
    
                total = total+1
                asig_total = asig_total+1
                if (tipoDatos=="failpass"):
                    if (real==predict[0]):
                        totalaciertos = totalaciertos+1
                        asig_totalaciertos = asig_totalaciertos+1
                    if(real==1 and predict[0]==1):
                        asig_totalsuspaciertos = asig_totalsuspaciertos +1
                        totalsuspaciertos = totalsuspaciertos +1
                    if(predict[0]==1):
                        asig_totalsusppredict = asig_totalsusppredict +1
                        totalsusppredict = totalsusppredict +1
                    if(real==1):
                        asig_totalsusp = asig_totalsusp +1
                        totalsusp = totalsusp +1
                if (tipoDatos=="valornotas"):
                    if ((real>=5 and predict[0]>=5) or (real<5 and predict[0]<5)):
                        totalaciertos = totalaciertos+1
                        asig_totalaciertos = asig_totalaciertos+1                
                    if(real<5 and predict[0]<5):
                        asig_totalsuspaciertos = asig_totalsuspaciertos +1
                        totalsuspaciertos = totalsuspaciertos +1
                    if(predict[0]<5):
                        asig_totalsusppredict = asig_totalsusppredict +1
                        totalsusppredict = totalsusppredict +1
                    if(real<5):
                        asig_totalsusp = asig_totalsusp +1
                        totalsusp = totalsusp +1
            
            
            
            resultStr = tipo +";"+ tipoDatos +";"+ str(asigEstudio) +";"+ str(asig_total) +";"+ str(asig_totalaciertos) +";"+ str(asig_totalsuspaciertos) +";"+ str(asig_totalsusppredict) +";"+ str(asig_totalsusp) +";"+ str(float(asig_totalsusp)/float(asig_total)) +";"+ str(float(asig_totalaciertos)/float(asig_total)) +";"+ str(float(asig_totalsuspaciertos)/float(asig_totalsusppredict)) +";"+ str(float(asig_totalsuspaciertos)/float(asig_totalsusp)) +";"
    #        print("Estadísticas asignatura "+str(asigEstudio))
    #        print("Total "+str(asig_total))
    #        print("Aciertos "+str(asig_totalaciertos))
    #        print("Suspensos acertados "+str(asig_totalsuspaciertos))
    #        print("Suspensos predichos "+str(asig_totalsusppredict))
    #        print("Suspensos totales "+str(asig_totalsusp)+"\n")
    #        
    #        print("Ratio suspendidos "+str(float(asig_totalsusp)/float(asig_total)))
    #        print("Ratio aciertos "+str(float(asig_totalaciertos)/float(asig_total)))
    #        print("Precision "+str(float(asig_totalsuspaciertos)/float(asig_totalsusppredict)))
    #        print("Recall "+str(float(asig_totalsuspaciertos)/float(asig_totalsusp))+"\n\n")
            print(resultStr)

            
        resultStr = tipo +";"+ tipoDatos +";"+ "GEIN" +";"+ str(total) +";"+ str(totalaciertos) +";"+ str(totalsuspaciertos) +";"+ str(totalsusppredict) +";"+ str(totalsusp) +";"+ str(float(totalsusp)/float(total)) +";"+ str(float(totalaciertos)/float(total)) +";"+ str(float(totalsuspaciertos)/float(totalsusppredict)) +";"+ str(float(totalsuspaciertos)/float(totalsusp)) +";"        
#print("Estadísticas final estudio")
#print("Total "+str(total))
#print("Aciertos "+str(totalaciertos))
#print("Suspensos acertados "+str(totalsuspaciertos))
#print("Suspensos predichos "+str(totalsusppredict))
#print("Suspensos totales "+str(totalsusp)+"\n")
#        
#print("Ratio suspendidos "+str(float(totalsusp)/float(total)))
#print("Ratio aciertos "+str(float(totalaciertos)/float(total)))
#print("Precision "+str(float(totalsuspaciertos)/float(totalsusppredict)))
#print("Recall "+str(float(totalsuspaciertos)/float(totalsusp))+"\n\n")
        print(resultStr)

    
outfile.close()

