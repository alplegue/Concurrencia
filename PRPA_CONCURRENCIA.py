# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 22:38:22 2023

@author: Álvaro Pleguezuelos Escobar
"""

from time import sleep

from multiprocessing import Semaphore

from multiprocessing import Process

from multiprocessing import Array

import random

from multiprocessing import current_process

numero_productores = 7

N = 5

tamaño_queue = 5


def get_data(queue):
    
    other = [0] * len(queue)
    
    maximum = max(queue)
    
    for i in range(len(queue)):
        
        if queue[i] == -1:
            
            other[i] = maximum + 1
            
        else:
            
            other[i] = queue[i]
            
    min_queue = other[0]
    
    position = 0
    
    for i in range(1, len(other)):
        
        if other[i] < min_queue and other[i] != -1:
            
            min_queue = other[i]
            
            position = i
            
    return min_queue, position

def add_data(queue, pid, data): 
    
    queue[pid] = data


def producer(queue, pid, sem_empty, sem_full, running, N_prod):
    
    v = random.randint(0, 5)
    
    while running[pid]:
        
        print(f"Productor {current_process().name} produciendo")
        
        sleep(random.random() / 3)
        
        v += random.randint(0, 5)
        
        sem_empty[pid].acquire()
        
        add_data(queue, pid, v)
        
        print(f"Productor {current_process().name} almacenando {v}")
        
        sem_full[pid].release()
        
        N_prod[pid] -= 1
        
        if N_prod[pid] == 0:
            
            queue[pid] = -1
            
            running[pid] = 0
            
            print(f"Productor {current_process().name} terminado")

def merge(queue, sem_empty, sem_full, running, result):
    
    for i in range(numero_productores):
        
        sem_full[i].acquire()
        
    while 1 in running:
        
        print(f"Consumidor {current_process().name} consumiendo")
        
        data, position = get_data(queue)
        
        sem_empty[position].release()
        
        print(f"Consumidor {current_process().name} ha consumido {data}")
        
        result.append(data)
        
        sleep(random.random() / 3)
        
        sem_full[position].acquire()
        
    print(f"{current_process().name} no puede seguir consumiendo, todos los productores han terminado")
    
    print("Queue final:", queue[:])
    
    print("Resultado final:", result)
    

def main():
    
    queue = Array('i', [-1] * (numero_productores * tamaño_queue))
    
    running = Array('i', numero_productores)
    
    N_prod = Array('i', numero_productores)
    
    for i in range(numero_productores):
        
        running[i] = 1
        
        N_prod[i] = N
        
    print("Queue incial:", queue[:])

    sem_empty_arr = []
    
    sem_full_arr = []
    
    for i in range(numero_productores):
        
        empty_arr = Semaphore(tamaño_queue)
        
        full_arr = Semaphore(0)
        
        sem_empty_arr.append(empty_arr)
        
        sem_full_arr.append(full_arr)

    result = []
    
    merge_list = [Process(target=merge,name="merge",args=(queue, sem_empty_arr, sem_full_arr, running, result))]

    producer_list = [Process(target=producer,name=f'prod_{i}',args=(queue, i, sem_empty_arr, sem_full_arr, running, N_prod))for i in range(numero_productores)]

    for p in producer_list + merge_list:
        p.start()

    for p in producer_list + merge_list:
        p.join()

if __name__ == "__main__":
    
    main()