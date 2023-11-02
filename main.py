import pandas as pd
import tkinter.filedialog as filedialog
class Particiones (object):
    def __init__(self,tam,bloq,FI) :
        self.tam = int(tam)  #tamaño parti 
        self.bloq = bloq # esta usada o no
        self.FI = int(FI) # frag interna
    

class Proceso (object):
    def __init__(self,id,ta,ti,tam,paso) :
        self.id = str (id)
        self.ta = int (ta)
        self.ti = int (ti)
        self.tam = int (tam)
        self.paso = int (paso)

file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
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
                print("Error: Al menos un proceso tiene un tamaño mayor a  250.")
                bandera = 0  # Establecer la bandera en 0
            elif num_filas > 10:
                print("Error: El número de procesos supera los 10.")
                bandera = 0  # Establecer la bandera en 0
            else:
                arch = df_ordenado
                bandera = 1  # Establecer la bandera en 1 si todo está en orden
                list_nuevo = []
                list_nuevo2 = []
                
                # Acceder a la columna 'TA' de la primera fila
                
                acumulador_ti = 0
                # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
                for index, row in df_ordenado.iterrows():
                    id = str(row['ID'])
                    ta = int(row['TA'])
                    ti = int(row['TI'])
                    tam = int(row['TAM'])
                    paso = 0
                    acumulador_ti += ti
                    proceso = Proceso(id,ta,ti,tam,paso)
                    list_nuevo.append(proceso)
                    list_nuevo2.append (proceso)
                
                info = []
                for i in range (0, len(list_nuevo2)):
                    info.append(list_nuevo2[i].id)
                print (f"cola de nuevos2 {info}")

                print("\n")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            bandera = 0  # Establecer la bandera en 0 en caso de error


#colas
list_listo = []
list_listo_susp = []
list_termi = []
list_ejec = []
gant = []
 


if bandera ==1:
    while (len (list_termi) != len(list_nuevo2)):
        if (len(list_listo) <6):#ver dsp
            if (len(list_nuevo)!=0):
                entra_a_listo = list_nuevo.pop(0)
                id= entra_a_listo.id
                ta = entra_a_listo.ta
                ti = entra_a_listo.ti
                tam= entra_a_listo.tam
                paso = 0
                proceso = Proceso(id,ta,ti,tam,paso)
                list_listo.append(proceso)  #agregar en q tiempo entra cola listo
                
            else:  
                tiempo = list_listo[0].ta
                while (len(list_termi) != len (list_nuevo2)):
                    prox = list_listo[1] #prox proceso
                    proceso_cargar = list_listo.pop (0)  #pop del primero de cola de listo
                   
                    if (proceso.paso == 0): # es la primera pasada del proceso
                        if (proceso_cargar.ta == tiempo): #perfecto damos prioridad
                            
                            print (f"Tiempo: {tiempo}, proceso {proceso_cargar.id} entra a ejecutarse")
                            q = tiempo  #tiempo es mi reloj general
                            ti_aux = proceso_cargar.ti
                        
                            #ver desp el if de arriba
                            quantum = 0  #es el quantum de round robin
                            while (ti_aux> 0 and quantum !=2):
                                quantum = quantum+1
                                ti_aux = ti_aux - 1
                                proceso_cargar.ti = ti_aux
                                gant.insert(q,proceso_cargar)
                                q=q+1
                                

                            if (ti_aux == 0): #lo mando a terminado
                                print (f"Tiempo: {q}, {proceso_cargar.id} termino ejecucion")
                                list_termi.append (proceso_cargar)    #falta sacar proceso de lista_nuevo2

                                for i in range (0,len(list_nuevo2)):
                                    if (list_nuevo2[i].id == proceso_cargar.id):
                                        list_nuevo2.pop(i)
                                        break

                            else:                             
                                proceso_cargar.ti = ti_aux
                                proceso_cargar.paso = 1
                                print (f"Tiempo: {q}, {proceso_cargar.id} termino ejecucion")
                                print (f"Al proceso {proceso_cargar.id} le quedan {ti_aux} para terminar su ejec")
                                
                                info=[]
                                for i in range (0,len(list_listo)):
                                    info.append(list_listo[i].id)
                                print ("cola de listos", info)
                                list_listo.append (proceso_cargar)
                        else:
                            proceso_cargar.paso = 1
                            list_listo.append(proceso_cargar)
                           
                            
                    else:
                        #hay que ejecutarlo nomas
                        q = tiempo  #tiempo es mi reloj general
                        ti_aux = proceso_cargar.ti
                        print (f"Tiempo: {tiempo}, proceso {proceso_cargar.id} entra a ejecutarse")
                        #ver desp el if de arriba
                        quantum = 0  #es el quantum de round robin
                        while (ti_aux> 0 and quantum !=2):
                            quantum = quantum+1
                            ti_aux = ti_aux - 1
                            proceso_cargar.ti = ti_aux
                            gant.insert (q,proceso_cargar)
                            q=q+1
                            

                        if (ti_aux == 0): #lo mando a terminado
                            print (f"Tiempo: {q}, {proceso_cargar.id} termino ejecucion")
                            list_termi.append (proceso_cargar)    #falta sacar proceso de lista_nuevo2

                            for i in range (0,len(list_nuevo2)):
                                if (list_nuevo2[i].id == proceso_cargar.id):
                                    list_nuevo2.pop(i)
                                    break

                        else:                             
                            proceso_cargar.ti = ti_aux
                            print(f"el proceso {proceso_cargar.id} entra en ejecucion")
                            print (f"Al proceso {proceso_cargar.id} le quedan {ti_aux} para terminar su ejec")
                            print("165")
                            list_listo.append (proceso_cargar)
                            info=[]
                            for i in range (0,len(list_listo)):
                                info.append(list_listo[i].id)
                            print ("cola de listos", info)
                
                            
                    tiempo = q 



                    """         p2ls p3ls   
                    P1  0  2    |p1|p1|p4|p4|p2|p2|p5|p5|               cola de listo: p3 p2 p4
                    P2  0  3     p1 p1 
                    P3  1  3                                cola listo:     p2 p3 p4 
                    P4   2  4
                    P5   6  3
                    """




                        
                    """else:
                        #debo buscar uno para darle prioridad 

                        print (f"lala {proceso_cargar.id}")
                        list_listo.append (proceso_cargar)
                        info=[]
                        for i in range (0,len(list_listo)):
                            info.append(list_listo[i].id)
                        print ("cola de listos", info)
                        ## aca deberia de recorrer la cola y ver si no hay ta siguiente igual a mi q actual
                        hago = 1
                        print ("ya entre al else")
                        for m in range (tiempo,acumulador_ti,2):
                            
                            for i in range (0,len(list_listo)):
                                if (tiempo == list_listo[i].ta) :
                                    hago = 0  #significa que NO HAGO lo de abajo, ya que en la cola hay alguno que tenga un ta igual mi q actual
"""
                    