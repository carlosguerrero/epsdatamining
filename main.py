# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:09:20 2016

@author: carlos

Este archivo genera una serie de archivos CSV a partir de los datos que nos encontramos en la base de datos.
Estos archivos CSV son generados en función de la configuración indicada en la clase ExperimentSetup.

"""

import CsvExpediente
import ExperimentSetup


expsetup = ExperimentSetup.ExperimentSetup("geinPreExpedienteTodosExclusive2")
print(expsetup.listadoAssigEstudio)

for asigEstudio in expsetup.listadoAssigEstudio:
    print(asigEstudio)
    expsetup.initAsigEstudio(asigEstudio)
    csv=CsvExpediente.CsvExpediente(expsetup)
    csv.generarMatriz()
    csv.escribirCsv()
    

