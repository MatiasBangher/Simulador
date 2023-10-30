import pandas as pd
import tkinter.filedialog as filedialog
class Particiones (object):
    def __init__(self,tam,bloq,FI) :
        self.tam = int(tam)
        self.bloq = 0
        self.FI = int(FI)

class Proceso (object):
    def __init__(self,id,ta,ti,tam) :
        self.id = str (id)
        self.ta = int (ta)
        self.ti = int (ti)
        self.tam = int (tam)

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
                
                # Acceder a la columna 'TA' de la primera fila
                

                # Recorrer el DataFrame y agregar IDs de procesos a la lista de nuevos procesos
                for index, row in df_ordenado.iterrows():
                    id = str(row['ID'])
                    ta = int(row['TA'])
                    ti = int(row['TI'])
                    tam = int(row['TAM'])
                
                    proceso = Proceso(id,ta,ti,tam)
                    list_nuevo.append(proceso)
                
                info = []
                for i in range(0,len(list_nuevo)):
                    info.append(list_nuevo[i].id)

                print(f"Lista de nuevos: {info}")
                print("\n")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            bandera = 0  # Establecer la bandera en 0 en caso de error


#colas
list_listo = []
list_listo_susp = []
list_termi = []

#memoria
so = 100
part1 = Particiones(60,0,0)
part2 = Particiones(120,0,0)
part3 = Particiones(250,0,0)
mem = [so,part1,part2,part3] 

list_nuevo2 = list_nuevo
control_mult=[]

# [1,2,3,4,5,6]  -- termi [0]
# [1] - listo 
j = 0
while (len(list_termi) != len(list_nuevo)):
    if (len(list_nuevo) < 6) :
        list_listo.append(list_nuevo[j])
        
    
        id = list_listo [j].id
        ta = list_listo [j].ta
        ti = list_listo [j].ti
        tam = list_listo [j].tam
            
        proceso = Proceso(id,ta,ti,tam)  
        ## aca arranca best fit
        parti = []  # Lista para almacenar las fragmentaciones internas positivas
        names = []  # Lista para almacenar los nombres correspondientes a las particiones

        rest1 = mem[1].tam - tam
        rest2 = mem[2].tam - tam 
        rest3 = mem[3].tam - tam


        if rest1 > 0 and (mem[1].bloq == 0):
            parti.append(rest1)
            names.append("part1")

        if rest2 > 0 and (mem[2].bloq == 0):
            parti.append(rest2)
            names.append("part2")

        if rest3 > 0 and (mem[3].bloq == 0) :
            parti.append(rest3)
            names.append("part3")

        if len(parti) != 0:  #si no hubo particiones va a cola de listo/susp
            minimo = min(parti)  # Buscar la mínima fragmentación interna
            posm = parti.index(minimo)  # Obtener la posición de la mínima fragmentación interna en parti
            pos = names[posm]  # Obtener el nombre de la partición correspondiente

            if pos == "part1":
                posn = 1  # Índice de la partición p1 en la lista particiones_mem
            elif pos == "part2":
                posn = 2  # Índice de la partición p2 en la lista particiones_mem
            else:
                posn = 3  # Índice de la partición p3 en la lista particiones_mem

            if (mem[posn].bloq == 0):
                resta = (mem[posn].tam - mem[posn].tam)+ minimo
                mem[posn].bloq = 1
                mem[posn].FI = resta


                list_listo.append(proceso)
                print(f"TIEMPO:{proceso.ta}")
                print(f"El proceso de id: {id}, entro en memoria, se encuentra en la particion {posn}")
                
                
            else:  
                list_listo_susp.append (proceso)
                
        else:
            list_listo_susp.append (proceso)
            

                ## fin best fit 
        print ("INFORMACION DE LAS PARTICIONES")
        for i in range(1, 4):  
            print (f"Particion {i}")

            if (mem[i].bloq == 1) :
                print (f"Tiene fragmentacion interna de: {mem[i].FI}, por lo que esta bloqueada")
            else:
                print ("Esta libre")

        
        #round robin
        if list_listo: 
            elim = list_listo.pop(0)
            entra = list_listo.pop(0)
            list_listo.remove (proceso)
            print (list_listo[0])
            
            
            print (f"El proceso {entra.id} entro en ejecucion")
            resta = entra.ti - 2
            if (resta <= 0): 
                
                print (f"proceso {entra.id} terminado")
                list_termi.append(entra.id)
            else:
                proceso = Proceso (entra.id,entra.ta,(entra.ti)-2,entra.tam)
                print (f"Al proceso {proceso.id} le queda {proceso.ti} de tiempo para terminar su ejecucion")
                list_listo.append(proceso) 
    
        ## fin round robin 
        info = []
        for i in range (0,len(list_listo)):
            info.append (list_listo[i].id)
        print (f"Cola de listos")
        print (info)
        info = []
        for i in range (0,len(list_listo_susp)):
            info.append (list_listo_susp[i].id)
        print (f"cola de listos suspendidos {info}")
        j = j + 1

   