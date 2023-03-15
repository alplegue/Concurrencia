import random
from multiprocessing import Process, BoundedSemaphore, Semaphore, Array

NPROD = 5
NCONS = 1
N = 8

def minimo(lista):
    i = 0
    while lista[i] == -1:
        i = i+1
    minimo = lista[i]
    prod = i
    for j in range(prod, len(lista)):
        if lista[j] < minimo and lista[j] != -1:
            minimo = lista[j]
            prod = j
    return minimo, prod
    

def productor(lista, buffer, prod):
     num = 0
     for k in range(N):
         num += random.randint(0,9)
         lista[2*prod].acquire()
         print('El productor', prod, 'produce el número', num,', lleva', k, 'numeros producidos')
         buffer[prod] = num
         lista[2*prod+1].release() 
     num = -1
     lista[2*prod].acquire()
     buffer[prod] = num
     lista[2*prod+1].release()
     


def consumidor(lista, buffer):  
    lista_ordenada = []
    for i in range(NPROD):
        lista[2*i+1].acquire()  
    while list(buffer) != [-1]*NPROD:
        num, prod = minimo(buffer)
        print('El consumidor toma el número', num, 'del productor', prod)
        lista_ordenada.append(num)
        print (f"lista: {lista_ordenada}")
        lista[2*prod].release()
        lista[2*prod + 1].acquire()
    print ('Valor final de la lista:', lista_ordenada)
    
    

def main():
     buffer = Array('i', NPROD)
     lista_sem = []
     for i in range(NPROD):
         lista_sem.append(BoundedSemaphore(1))
         lista_sem.append(Semaphore(0)) 
     lp = []
     for prod in range(NPROD):
         lp.append(Process(target=productor, args=(lista_sem, buffer, prod)))
     lp.append(Process(target=consumidor, args=(lista_sem, buffer)))    
     for p in lp:
         p.start()
     for p in lp:
         p.join()

if __name__ == "__main__":
 main()    