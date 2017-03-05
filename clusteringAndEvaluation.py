import pandas as pd
from sklearn.cluster import KMeans
import ExperimentSetup

expsetup = ExperimentSetup.ExperimentSetup("geinPreExpedienteTodosExclusive2")
nombreDirectorio = "../csvFiles/"+expsetup.nombreExperimento+"/"
outfile=open('clusteringresults.txt','w')

for tipo in ["all", "nota", "convocatorias"]:
    if tipo=="all":
        num_colum_title=3
    else:
        num_colum_title=2
    for asigEstudio in expsetup.listadoAssigEstudio:
        # Read in the csv file
        aprobados = pd.read_csv(nombreDirectorio+str(asigEstudio)+tipo+".csv")
        
        print(aprobados.shape)
        
        print(pd.value_counts(aprobados.iloc[:,num_colum_title:].values.ravel()))
        
        
        for kn in range(1,10):
            kmeans =  KMeans(n_clusters=kn, random_state=1)
            kmeans_model = kmeans.fit(aprobados.iloc[:, 1:])
            #mostramos, para cada muestra, en el cluster que ha sido encajado, desde el 0 hasta el n_clusters
            labels = kmeans_model.labels_
            #print(kmeans_model.labels_)
            #mostramos los centroides de cada cluster
            #print(kmeans_model.cluster_centers_)
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