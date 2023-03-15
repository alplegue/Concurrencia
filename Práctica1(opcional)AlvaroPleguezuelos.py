import random
from multiprocessing import Process, BoundedSemaphore, Semaphore, Lock, Array

NPROD = 5
NCONS = 1
k = 2
N = 3


def minimo(lista):
    aux = []
    for l in range(NPROD):
        aux.append(lista[k*l])
    i = 0
    while aux[i] == -1:
        i = i+1
    minimo = aux[i]
    prod = i
    for j in range(prod, len(aux)):
        if aux[j] < minimo and aux[j] != -1:
            minimo = aux[j]
            prod = j
    return minimo, prod    
   


def add_data(mutex, buffer, prod, productos, num):
    mutex.acquire() 
    try:
        buffer[k*prod + productos[prod]] = num
        productos[prod]+=1
        print("buffer:", list(buffer))
    finally:
        mutex.release() 


def get_data(mutex, buffer, productos, lista_ordenada):
    mutex.acquire()
    try:
        num, prod = minimo(buffer)
        print('El consumidor toma el número', num, 'del productor', prod)
        lista_ordenada.append(num)
        for i in range(productos[prod] - 1):
            buffer[prod*k + i] = buffer[prod*k + (i+1)]
        productos[prod] -= 1
    finally:
        mutex.release() 
    return num, prod



def productor(lista, mutex, buffer, prod, productos):
     num = 0
     for l in range(N):
         num += random.randint(0,9)
         lista[2*prod].acquire()
         print('El productor', prod, 'produce el número', num,', lleva', l+1, 'numeros producidos')
         add_data(mutex, buffer, prod, productos, num)
         lista[2*prod+1].release()
     num = -1
     lista[2*prod].acquire() 
     add_data(mutex, buffer, prod, productos, num)
     lista[2*prod+1].release() 
     

def consumidor(lista, mutex, buffer, productos):  
    lista_ordenada = []
    for i in range(NPROD):
        lista[2*i+1].acquire() 
    while [buffer[i] for i in range(0,len(buffer))]!=[-1]*(NPROD*k):
        num, prod = get_data(mutex, buffer, productos, lista_ordenada)
        lista[2*prod].release() 
        lista[2*prod + 1].acquire() 
        print(f"lista: {lista_ordenada}")
    print ('Valor final de la lista:', lista_ordenada)

def main():
     buffer = Array('i', NPROD*k)
     productos = Array('i', NPROD)
    
     lista_sem = []
     for i in range(NPROD):
         lista_sem.append(BoundedSemaphore(k))
         lista_sem.append(Semaphore(0)) 
     mutex = Lock() 
     lp = []
     for prod in range(NPROD):
         lp.append(Process(target=productor, args=(lista_sem, mutex, buffer, prod, productos)))
     lp.append(Process(target=consumidor, args=(lista_sem, mutex, buffer, productos)))    
     
     for p in lp:
         p.start()
     for p in lp:
         p.join()

if __name__ == "__main__":
 main() 