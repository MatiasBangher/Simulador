import pandas as pd
import tkinter.filedialog as filedialog
import time


def Best_FIT ():
    ## aca arranca best fit
    parti = []  # Lista para almacenar las fragmentaciones internas positivas
    names = []  # Lista para almacenar los nombres correspondientes a las particiones
    
    rest1 = mem[1].tam - entra_a_listo.tam
    rest2 = mem[2].tam - entra_a_listo.tam 
    rest3 = mem[3].tam - entra_a_listo.tam


    if rest1 > 0 :
        parti.append(rest1)
        names.append("part1")
        

    if rest2 > 0 :
        parti.append(rest2)
        names.append("part2")
        

    if rest3 > 0  :
        parti.append(rest3)
        names.append("part3")
    minimo = min(parti)  # Buscar la mínima fragmentación interna
    
    posm = parti.index(minimo)  # Obtener la posición de la mínima fragmentación interna en parti
    pos = names[posm]  # Obtener el nombre de la partición correspondiente

    if pos == "part1":
        posn = 1  # Índice de la partición p1 en la lista particiones_mem
    elif pos == "part2":
        posn = 2  # Índice de la partición p2 en la lista particiones_mem
    else:
        posn = 3  # Índice de la partición p3 en la lista particiones_mem
  
    if (mem[posn].bloq == 0): #no esta bloqueada la mejor particion
        
        resta = (mem[posn].tam - mem[posn].tam)+ minimo
        mem[posn].FI = resta
        mem[posn].bloq = 1 
        mem[posn].proc = entra_a_listo.id  #cargo el id del proceso cargado en esa parti, importante para el cuadro
        list_listo.append (entra_a_listo)
        print('| {:<15} | {:<15} | {:<15} Kb|'.format(mem[posn].proc,posn, mem[posn].FI))
        list_nuevo.pop(0) 
    else: #buscar la primera libre que entre el proceso 
        cargado = "no"
        for i in range (1,4):
            if (mem[i].bloq == 0):#particion libre
                resta = mem[i].tam - entra_a_listo.tam
                if resta > 0 : # puede entrar el loko porque da una fragmentacion mayor a 0
                    
                    mem[i].FI = resta
                    mem[i].bloq = 1
                    mem[i].proc = entra_a_listo.id
                    print('| {:<15} | {:<15} | {:<15} |'.format('Id Proceso','Particion', 'Frag. Interna'))
                    print('| {:<15} | {:<15} | {:<15} Kb  |'.format(mem[i].proc,i, mem[i].FI ))
                    list_listo.append (entra_a_listo)
                    list_nuevo.pop(0)
                    
                    cargado = "si"
                    break #rompo el for 
        if cargado == "no" :
            if (len(list_listo_susp)<2):  #salio del for, no encontro ninguna particion disponible, lo mando a list y susp si es que hay espacio
                a_listo_susp = list_nuevo.pop(0)
                print (f"entra a susp:{a_listo_susp.id}")
                list_listo_susp.append (a_listo_susp)
             #si en la lista de suspendidos hay mas de 2, va a seguir en nuevo, nunca hace el pop
            

class Particiones (object):
    def __init__(self,tam,bloq,FI,proc) :
        self.tam = int(tam)  #tamaño parti 
        self.bloq = bloq # esta usada o no
        self.FI = int(FI) # frag interna
        self.proc = str (proc)
    

class Proceso (object):
    def __init__(self,id,ta,ti,tam) :
        self.id = str (id)
        self.ta = int (ta)
        self.ti = int (ti)
        self.tam = int (tam)

class Info_irrupcion (object):  #lo creo para calcular TE
    def __init__(self,id,ti):
        self.id = str (id)
        self.ti = int (ti)
        
print ("Bienvenido al SIMULADOR DE PROCESOS")
    ## aca arranca el programa realizando la carga del archvio

bandera=0    
file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  #solo busca uno que termina en .csv
if file_path:
    try:
        # Cargar el archivo CSV usando pandas con el delimitador correcto (;)
        df = pd.read_csv(file_path, delimiter=';')
        # Ordenar el DataFrame por la columna "TA" de menor a mayor
        df_ordenado = df.sort_values(by='TA')
        
        # Contar el número de filas en el DataFrame ordenado
        num_filas = df_ordenado.shape[0]
        

        # Verificar si el número de filas supera las 10
        if df_ordenado['TAM'].max() > 250:
            print("Error: Al menos un proceso tiene un tamaño mayor a  250k.")
            bandera = 0  # Establecer la bandera en 0
        elif num_filas > 10:
            print("Error: El número de procesos supera los 10.")
            bandera = 0  # Establecer la bandera en 0
        else:
            
            bandera = 1  # Establecer la bandera en 1 si todo está en orden
            
            list_nuevo = []
            tiempo_irrupciones = []
            acumulador_ti = 0
            nro_proc = 0
            # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
            for index, row in df_ordenado.iterrows():
                nro_proc = nro_proc + 1
                id = str(row['ID'])
                ta = int(row['TA'])
                ti = int(row['TI'])
                tam = int(row['TAM'])
                acumulador_ti += ti
                proceso = Proceso(id,ta,ti,tam)
                list_nuevo.append(proceso)
                irrupcion = Info_irrupcion (id,ti)  #creo una clase con id y tiempo de irrupcion del proceso
                tiempo_irrupciones.append (irrupcion) # guardo la clase en un array

            
            info = []
            for i in range (0, len(list_nuevo)):
                info.append(list_nuevo[i].id)
            print (f"Tiempo 0 -> cola de nuevos: {info}")
            print("\n")
            tiempo = list_nuevo[0].ta  #tiempo de inicio del programa


            
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        bandera = 0  # Establecer la bandera en 0 en caso de error

#colas
list_listo = []
list_listo_susp = []
list_termi = []
list_ejec = []

acumtrp = 0  #para trp
acumEspera = 0 #para tiempo de espera promedio

#memoria
so = 100  #sist op
part1 = Particiones(60,0,0,"")
part2 = Particiones(120,0,0,"")
part3 = Particiones(250,0,0,"")
mem = [so,part1,part2,part3]  #array de memoria
band=0
if bandera ==1:
    
    while (len(list_termi)!= nro_proc):  #ciclo principal
        print (f"Tiempo: {tiempo}")  #informe de tiempo
        if band==0:
            print('MEMORIA')
            print('| {:<15} | {:<15} | {:<15} |'.format('Id Proceso','Particion', 'Frag. Interna'))
            band=1 
        if (len(list_nuevo)>0):  #si hay alguno en la cola de nuevo 
            while tiempo == list_nuevo[0].ta:  #si su tiempo de arribo es igual a mi tiempo actual veo que hacer, con el ciclo proceso todos los procesos los cuales sus TA = tiempo actual
                if (len(list_listo)<3):  # hay espacio en cola de listos
                    entra_a_listo = list_nuevo[0] # no hago pop todavia, si el proceso puede entrar a una particion, recien hace pop en el procedimiento BEST FIT linea 48 y 60
                    Best_FIT ()
                    if (len(list_nuevo)==0):  #si hizo un pop en el best fit, y nuevos quedo a 0 rompemos el ciclo de la linea 170
                        break
                else:  #si no hay espacio en listos, me fijo en susp
                    if (len(list_listo_susp)<2): #hay espacio
                        a_listo_susp = list_nuevo.pop(0)  #ahi si hago pop y lo mando a susp
                        print (f"a list susp: {a_listo_susp.id}")
                        list_listo_susp.append (a_listo_susp)  
                    else:  #si no entro x ningun lado, rompo el ciclo, dejando ese o esos procesos en nuevo aun 
                        break
        if (len (list_listo) > 0):   #si hay alguno en listos lo ejecutamos
            ejecutar = list_listo[0]  #no hago pop de lista de listo todavia, OJO: EN LA TEORIA SI UNO SE EJECUTA SALE DE LISTO, pero a fines practicos nosotros lo mantenemos
            ti_aux = ejecutar.ti   
            quantum = 0  #es el quantum de round robin
            while (ti_aux > 0 and quantum !=2):
                if (len(list_nuevo)>0):  #si en el mismo tiempo que el  entra a ejecutar, puede ser el TA de un proceso nuevo, hace lo mismo q lin 152
                    while tiempo == list_nuevo[0].ta: #arriba uno o varios proceso
                        if (len(list_listo)<3):  
                            entra_a_listo = list_nuevo[0]
                            Best_FIT ()
                            if (len(list_nuevo) == 0):
                                break
                        else:
                            if (len(list_listo_susp)<2):
                                a_listo_susp = list_nuevo.pop(0)
                                print (f"entra susp:{a_listo_susp.id}")
                                list_listo_susp.append (a_listo_susp)
                                if len (list_nuevo) == 0:  #si ya me comi todos los proceso rompo el while
                                    break
                            else:  #si no entro x ningun lado rompo el while pq sino entra en bucle infinito, 
                                break
                print (f"Proceso: {ejecutar.id} entra a ejecucion")
                quantum = quantum+1  #cosas obvias las que hago aca
                ti_aux = ti_aux - 1
                ejecutar.ti = ti_aux
                tiempo = tiempo + 1

            
            if (ti_aux==0): #el PROCESO se termino de ejecutar, libero memoria y cola de listo
                print (f"El proceso {ejecutar.id} termino de ejecutarse")
                calculoR = tiempo - ejecutar.ta  #calculo de TR
                
                acumtrp= calculoR + acumtrp  #para TRP
                for i in range (0,len (tiempo_irrupciones)):  #busco en mi array de irrupciones el TI de este proceso
                    if tiempo_irrupciones[i].id == ejecutar.id :  #si los id coinciden estoy en ese proceso
                        calculoE = calculoR - tiempo_irrupciones[i].ti  #hago el calculo de Espera
                        break
                
                
                acumEspera = calculoE + acumEspera  #calculo de TEP
                list_listo.pop(0)  #aca recien hago el pop , no lo hago en la 161
                for j in range (1,4):  #busco en las particiones para liberarlo
                    
                    if mem[j].proc == ejecutar.id: # libero la particion, pq encontro al proceso
                        mem[j].proc = ""
                        mem[j].bloq = 0
                        mem[j].FI = 0
                        print (f"Se libero particion {j}")
                        list_termi.append (ejecutar.id)  #lo mando a terminado
                        
                        
                        salio = "no"
                        susp = 0
                        nuevo = 0
                        if (len(list_listo_susp)>0):   #si hay alguno en listo y susp, lo saco de ahi PRIORIDAD TOMADA X EL GRUPO
                            sale = list_listo_susp[0] #saco al primero de listo y susp y lo mando a listo (no hago pop tdv pq debo buscar particion)
                            salio = "si"
                            
                            susp = 1
                        else:  # si no hay ninguno de ahi lo saco de nuevo
                            if (len(list_nuevo)>0 ):
                                sale = list_nuevo[0]
                                salio = "si"
                                nuevo = 1
                        
                        ###best fit pero jugando con lista de listos_susp <- IMPORTANTE
                        if (salio == "si") : #significa que salio o de nuevo o de listo
                            parti = []  # Lista para almacenar las fragmentaciones internas positivas
                            names = []  # Lista para almacenar los nombres correspondientes a las particiones
                
                            rest1 = mem[1].tam - sale.tam
                            rest2 = mem[2].tam - sale.tam 
                            rest3 = mem[3].tam - sale.tam
                            if rest1 > 0 :
                                parti.append(rest1)
                                names.append("part1")
                            if rest2 > 0 :
                                parti.append(rest2)
                                names.append("part2")
                            if rest3 > 0  :
                                parti.append(rest3)
                                names.append("part3")
                            minimo = min(parti)  # Buscar la mínima fragmentación interna
                            posm = parti.index(minimo)  # Obtener la posición de la mínima fragmentación interna en parti
                            pos = names[posm]  # Obtener el nombre de la partición correspondiente

                            if pos == "part1":
                                posn = 1  # Índice de la partición p1 en la lista particiones_mem
                            elif pos == "part2":
                                posn = 2  # Índice de la partición p2 en la lista particiones_mem
                            else:
                                posn = 3  # Índice de la partición p3 en la lista particiones_mem

                            
                            if (mem[posn].bloq == 0): #no hay nada  
                                
                                resta = (mem[posn].tam - mem[posn].tam)+ minimo
                                mem[posn].FI = resta
                                mem[posn].bloq = 1
                                mem[posn].proc = sale.id
                                list_listo.append (sale)#al que salio de list y susp lo mando a listo, pq encontro particion
                                print('MEMORIA')
                                print('| {:<15} | {:<15} | {:<15} |'.format('Id Proceso','Particion', 'Frag. Interna'))
                                print('| {:<15} | {:<15} | {:<15}kb |'.format(mem[posn].proc,i, mem[posn].FI ))
                                if susp == 1:
                                    
                                    list_listo_susp.pop(0)  #aca recien hago pop pq encontro particion
                                else:
                                    if nuevo ==1:
                                        list_nuevo.pop (0)
                            
                                if (len(list_listo_susp)<2):  # si en mi lista de susp hay 0 o 1 proceso 
                                    
                                    if (len(list_nuevo)>0): #si queda alguno en nuevos lo mando a listo_susp
                                        
                                        entra_a_susp = list_nuevo.pop (0)  #aca hago el pop
                                        print (f"entra a susp: {entra_a_susp.id}")
                                        list_listo_susp.append (entra_a_susp)
                            else: #buscar una libre y chau
                                for i in range (1,4):
                                    if (mem[i].bloq == 0): #particion libre
                                        
                                        resta = mem[i].tam - sale.tam
                                        if resta > 0 : # puede entrar el loko
                                            mem[i].FI = resta
                                            mem[i].bloq = 1
                                            mem[i].proc = sale.id
                                          
                                           
                                            list_listo.append (sale)

                                            if susp == 1:
                                                print ("pop de susp")
                                                list_listo_susp.pop(0)  #aca recien hago pop pq encontro particion , banderas para ver en cual hago el pop
                                            else:
                                                if nuevo ==1:
                                                    list_nuevo.pop (0)

                                            if (len(list_listo_susp)<2):  
                                                if (len(list_nuevo)>0):
                                                    entra_a_susp = list_nuevo.pop (0)
                                                    print (f"entra a list susp: {entra_a_susp.id}")
                                                    list_listo_susp.append (entra_a_susp)
                                            break #rompo el for 

            else: #el loko no termino su irrupcion lo mando al final de la cola de listo 
                list_listo.pop(0)
                print (f"Al proceso {ejecutar.id} le queda {ejecutar.ti} para terminar su ejecucion")
                list_listo.append (ejecutar)  #lo mando al final de cola de listos
                info = []
                for i in range (0, len(list_listo)):
                    info.append(list_listo[i].id)
                print (f"cola de listos {info}")
        else:  
            if (len(list_nuevo) >0): # corremos el tiempo hasta que arribe uno
                while (list_nuevo[0].ta != tiempo):
                    tiempo = tiempo + 1
        
        input("\nPresione enter para continuar...")

    #tiempo de retorno y espera para cada proceso y los respectivos tiempos promedios.
    
    trp = acumtrp / nro_proc 
    print (f"Tiempo de retorno promedio: {trp} unidades de tiempo")
    tep = acumEspera / nro_proc
    print (f"Tiempo de espera promedio: {tep} unidades de tiempo")
    
else:
    input("Hubo error, presione enter para finalizar...")

