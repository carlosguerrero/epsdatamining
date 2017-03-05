
def getClosestCentroid(centroides,sample):
    from scipy.spatial import distance
    import sys
    
    min_dst = sys.float_info.max
    id=0
    i=0
    
    for centro in centroides:
        dst = distance.euclidean(sample,centro)
        if dst<min_dst:
            min_dst = dst
            id=i
        i=i+1
    
    return id

def validatePrediction(asig,totcent,centroides,samples):
    

    #y = kmeans.cluster_centers_[1:2,:]
    #z = kmeans.cluster_centers_[:1,:]

    #dst = distance.euclidean(y,z)

    #print centroides
    outfileNotas=open('predictionNotas.txt','w')
    outfileBinario=open('predictionBinaria.txt','w')
    outfileResumen=open('predictionResumen.csv','a')
    outfileNotas.write(str(asig)+";"+str(totcent)+";alumno real;prediccion\n")
    outfileBinario.write(str(asig)+";"+str(totcent)+";alumno real;prediccion\n")
    #outfileResumen.write(str(asig)+";"+str(totcent)+";verdaderosaprobados;verdaderossuspendidos;falsosaprobados;falsossuspendidos\n")
    #outfileResumen.write(str(asig)+";"+str(totcent)+";alumnos;aprobados;totalaciertos;precisionaprobadosverdaderosaprobados;precisionsuspendidosverdaderossuspendidos;falsosaprobados;falsossuspendidos;")
    outfileResumen.write(str(asig)+";"+str(totcent)+";alumnos;aprobados;suspendidos;verdaderosaprobados;verdaderossuspendidos;falsosaprobados;falsossuspendidos;")
    muestras = samples.get_values()

    i=0
    falsosaprobados=0
    falsossuspendidos=0
    verdaderosaprobados=0
    verdaderossuspendidos=0
    aprobados=0
    
    for alumno in muestras:
        i=i+1
        iClosest = getClosestCentroid(centroides[:,1:], alumno[2:])
        outfileNotas.write(str(alumno[0])+";"+str(alumno[1])+";"+str(centroides[iClosest,0])+"\n")
        outfileBinario.write(str(alumno[0])+";")
        if alumno[1]<5: 
            outfileBinario.write(str(0)+";") 
        else:
            outfileBinario.write(str(1)+";")
        if centroides[iClosest,0]<5: 
            outfileBinario.write(str(0)+"\n") 
        else:
            outfileBinario.write(str(1)+"\n")         
        if (alumno[1]<5) and (centroides[iClosest,0]<5):
            verdaderossuspendidos=verdaderossuspendidos+1
        if (alumno[1]>=5) and (centroides[iClosest,0]<5):
            aprobados=aprobados+1
            falsossuspendidos=falsossuspendidos+1
        if (alumno[1]<5) and (centroides[iClosest,0]>=5):
            falsosaprobados=falsosaprobados+1
        if (alumno[1]>=5) and (centroides[iClosest,0]>=5):
            aprobados=aprobados+1
            verdaderosaprobados=verdaderosaprobados+1
             
    #outfileResumen.write(str(i)+";"+str(float(aprobados)/float(i))+";"+str(float(verdaderosaprobados)/float(i)+float(verdaderossuspendidos)/float(i))+";"+str(float(verdaderosaprobados)/float(i))+";"+str(float(verdaderossuspendidos)/float(i))+";"+str(float(falsosaprobados)/float(i))+";"+str(float(falsossuspendidos)/float(i))+"\n")        
    outfileResumen.write(str(i)+";"+str(aprobados)+";"+str(i-aprobados)+";"+str(verdaderosaprobados)+";"+str(verdaderossuspendidos)+";"+str(falsosaprobados)+";"+str(falsossuspendidos)+"\n")        
    outfileNotas.close()
    outfileBinario.close()
    outfileResumen.close()
    


import pandas as pd
from sklearn.cluster import KMeans
import ExperimentSetup

expsetup = ExperimentSetup.ExperimentSetup("geinPreExpedienteTodosExclusive2")
nombreDirectorio = "../csvFiles/"+expsetup.nombreExperimento+"/"
outfile=open('clusteringresults.txt','w')

import os
if os.path.exists('predictionResumen.csv'):
    os.remove('predictionResumen.csv')

#for tipo in ["all", "nota", "convocatorias"]:
for tipo in ["convocatorias"]:
    if tipo=="all":
        num_colum_title=3
    else:
        num_colum_title=2
    for asigEstudio in expsetup.listadoAssigEstudio:
        # Read in the csv file
        aprobados = pd.read_csv(nombreDirectorio+str(asigEstudio)+tipo+".csv")
        
        print(aprobados.shape)
        
        #print(pd.value_counts(aprobados.iloc[:,num_colum_title:].values.ravel()))
        print(pd.value_counts(aprobados.iloc[:,1:].values.ravel()))
        
        
        for kn in range(1,10):
            kmeans =  KMeans(n_clusters=kn, random_state=1)
            kmeans_model = kmeans.fit(aprobados.iloc[:, 1:])
            #mostramos, para cada muestra, en el cluster que ha sido encajado, desde el 0 hasta el n_clusters
            labels = kmeans_model.labels_
            
            validatePrediction(asigEstudio,kn,kmeans.cluster_centers_,pd.read_csv(nombreDirectorio+str(asigEstudio)+"C"+tipo+".csv"))            
            
            #print(kmeans_model.labels_)
            #mostramos los centroides de cada cluster
            print(kmeans_model.cluster_centers_)
            #mostramos una matriz en la que aparecen las columnas correspondiendo al numero de veces que se han presentado
            #y las filas, el grupo en el que ha sido clasificado. El valor de cada celda es cuantos hay de ese tipo.        
            if tipo=="nota":
                #print(pd.crosstab(labels,aprobados[str(asigEstudio)+"nota"]))
                outfile.write(str(pd.crosstab(labels,aprobados[str(asigEstudio)+"nota"])))
                outfile.write("\n")
            if tipo=="convocatorias":
                #print(pd.crosstab(labels,aprobados[str(asigEstudio)+"presentados"]))
                outfile.write(str(pd.crosstab(labels,aprobados[str(asigEstudio)+"presentados"])))
                outfile.write("\n")
            if tipo=="all":
                #print(pd.crosstab(labels,aprobados[str(asigEstudio)+"presentados"]))
                #print(pd.crosstab(labels,aprobados[str(asigEstudio)+"nota"]))
                outfile.write(str(pd.crosstab(labels,aprobados[str(asigEstudio)+"presentados"])))
                outfile.write("\n")
                outfile.write(str(pd.crosstab(labels,aprobados[str(asigEstudio)+"nota"])))
                outfile.write("\n")
outfile.close()

