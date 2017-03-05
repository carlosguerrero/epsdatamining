#!/usr/bin/python
# -*- coding: utf-8 -*-

class ExperimentSetup:



    def initAsigEstudio(self,i):
        self.asigEstudio=i
   
    def getSelectSentenceAllAssig(self):
        return self.selectSentenceAllAssig.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
       
    def getSelectSentenceAllAlu(self):
        return self.selectSentenceAllAlu.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
        
    def getSelectSentenceAnyoPrevioAluAprob(self):
        return self.selectSentenceAnyoPrevioAluAprob.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
       
    def getSelectSentenceAssigExpedienteAlu(self):
        return self.selectSentenceAssigExpedienteAlu.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
 
    def getSelectSentenceAnyoAprobAlu(self):
        return self.selectSentenceAnyoAprobAlu.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
       
    def getSelectSentenceAssigPredecir(self):
        return self.selectSentenceAssigPredecir.replace("[*ASIGACTUAL*]",str(self.asigEstudio))


    def getSelectSentenceAllAluActual(self):
        return self.selectSentenceAllAluActual.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
    def getSelectSentenceAnyoPrevioAluActual(self):
        return self.selectSentenceAnyoPrevioAluActual.replace("[*ASIGACTUAL*]",str(self.asigEstudio))
    def getSelectSentenceAnyoActualAluActual(self):
        return self.selectSentenceAnyoActualAluActual.replace("[*ASIGACTUAL*]",str(self.asigEstudio))

 
        
    def __init__(self, configName):

    #esta configuracion de experimento corresponde aquella en el que estudiamos todas las asignaturas de segundo
    #teniendo en cuenta los expedientes académicos de únicamente los alumnos que han aprobado (aprobados) la asignatura
    #incluyendo en su expediente los resultados del año en el que aprobaron el expediente (PostExpediente)
    #de las asignaturas de todos los cursos hasta el que se situa la asignatura a estudio inclusive (inclusive)  

        if configName =="geinPostExpedienteAprobadosInclusive":
            self.nombreExperimento = configName
            self.anyoEstudio =2014
            self.asigEstudio =21708
            self.asigCurso =2
            self.listadoAssigEstudio = [21708,21710,21711,21712,21713,21715,21716,21717,21718]
            #self.listadoAssigEstudio = [21708]
            #alumnos que se utilizan para llenar la KB            
            #seleccionamos a todos aquellos alumnos que tienen la asigntarua aprobada antes del anyoEstudio y miramos el anyo en que aprobaron.
            self.selectSentenceAllAlu="select id_alu,any from acta where (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig="+str(self.asigEstudio)+" and nota>5 order by id_alu;"
            #asignaturas que se utilizan en cada muestra de cada alumno de la KB            
            #seleccionamos las asginaturas de primero y segundo
            self.selectSentenceAllAssig="select distinct(assig) as codassig from acta where (pla='gein' or pla='gin2') and curs<="+str(self.asigCurso)+" and assig!=21719 order by assig;"

    #los expedidentes de los años antes de que se aprobara con las asignaturas solo de primero con todos los expedientes        
        
        if configName =="geinPreExpedienteTodosExclusive":
            self.nombreExperimento = configName
            self.anyoEstudio =2014
            self.asigEstudio =0
            self.asigCurso =2
            #self.listadoAssigEstudio = [21708,21710,21711,21712,21713,21715,21716,21717,21718]
            self.listadoAssigEstudio = [21708]
            #todos los alumnos a estudiar
            self.selectSentenceAllAlu="select id_alu,any,any from acta where (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] and nota>5 order by id_alu;"
            #todas las asignaturas a estudiar
            self.selectSentenceAllAssig="select distinct(assig) as codassig from acta where assig=[*ASIGACTUAL*] or ((pla='gein' or pla='gin2') and curs<"+str(self.asigCurso)+" and assig!=21719) order by assig;"
            #alumnos que se utilizan para llenar la KB            
            #seleccionamos a todos aquellos alumnos que tienen la asigntarua aprobada antes del anyoEstudio y miramos el anyo en que aprobaron.
            self.selectSentenceAnyoPrevioAluAprob="select id_alu,(any-1),any from acta where (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] and nota>5 order by id_alu;"
            #asignaturas que se utilizan en cada muestra de cada alumno de la KB            
            #seleccionamos las asginaturas de primero y segundo
            self.selectSentenceAssigExpedienteAlu="select distinct(assig) as codassig from acta where (pla='gein' or pla='gin2') and curs<"+str(self.asigCurso)+" and assig!=21719 order by assig;"

            self.selectSentenceAnyoAprobAlu="select id_alu,any,any from acta where (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] and nota>5 order by id_alu;"
            self.selectSentenceAssigPredecir="select distinct(assig) as codassig from acta where  assig=[*ASIGACTUAL*];"

        
        if configName =="geinPreExpedienteTodosExclusive2":
            self.nombreExperimento = configName
            self.anyoEstudio =2014
            self.asigEstudio =0
            self.asigCurso =2
            self.listadoAssigEstudio = [21708,21710,21711,21712,21713,21715,21716,21717,21718]
            #self.listadoAssigEstudio = [21708]
            #todos los alumnos a estudiar
            self.selectSentenceAllAlu="select id_alu,any,any from acta where id_alu not in (select id_alu from epsdatamining.acta where any="+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*]) and (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] group by id_alu,any order by id_alu;"
            #self.selectSentenceAllAlu="select id_alu,any,any from acta where (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] and nota>5 order by id_alu;"
            #todas las asignaturas a estudiar
            self.selectSentenceAllAssig="select distinct(assig) as codassig from acta where assig=[*ASIGACTUAL*] or ((pla='gein' or pla='gin2') and curs<"+str(self.asigCurso)+" and assig!=21719) order by assig;"
            #alumnos que se utilizan para llenar la KB            
            #seleccionamos a todos aquellos alumnos que tienen la asigntarua aprobada antes del anyoEstudio y miramos el anyo en que aprobaron.
            self.selectSentenceAnyoPrevioAluAprob="select id_alu,(any-1),any from acta where id_alu not in (select id_alu from epsdatamining.acta where any="+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*]) and (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] group by id_alu,any order by id_alu;"
            #asignaturas que se utilizan en cada muestra de cada alumno de la KB            
            #seleccionamos las asginaturas de primero y segundo
            self.selectSentenceAssigExpedienteAlu="select distinct(assig) as codassig from acta where (pla='gein' or pla='gin2') and curs<"+str(self.asigCurso)+" and assig!=21719 order by assig;"

            self.selectSentenceAnyoAprobAlu="select id_alu,any,any from acta where id_alu not in (select id_alu from epsdatamining.acta where any="+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*]) and (pla='gein' or pla='gin2') and any<"+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*] group by id_alu,any order by id_alu;"
            self.selectSentenceAssigPredecir="select distinct(assig) as codassig from acta where  assig=[*ASIGACTUAL*];"


            self.selectSentenceAllAluActual="select id_alu,any,any from epsdatamining.acta where any="+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*];"
            self.selectSentenceAnyoPrevioAluActual="select id_alu,(any-1),any from acta where any="+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*];"
            self.selectSentenceAnyoActualAluActual="select id_alu,any,any from acta where any="+str(self.anyoEstudio)+" and assig=[*ASIGACTUAL*];"
            
