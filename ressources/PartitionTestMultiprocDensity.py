"""
Title: Partition test density

Purpose: Given four integers L, l, m and q, a float delta in (0,1), this program
test with significance level delta which integers from l to L can be represented
as strict partitions into m integers raised to the power q.

The program realises for each integer n from L down to l parallel independent
random realisations of a sampler that has a success rate bounded by the Boltzmann
distribution described in https://arxiv.org/abs/2303.16960.

MIT License

Copyright (c) [2023] [Jean Peyen]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import multiprocessing as mp
import random
import numpy as np
from math import gamma, factorial, exp, log, floor
import time

#Sample strict partitions into m parts which are q-th powers smaller than L.
#z1 and z2 are calibration parameters for the sampler
def worker_sampler(q,L,n,m,z1,z2):
    part=[]
    N=0
    M=0
    j=1
    l=1
    while M<m and l<=n-N and l<=L:
        Z=(z1**l)*z2
        p=Z/(1+Z)
        if np.random.binomial(1, p):
            part.append(l)
            N=N+l
            M=M+1
        j=j+1
        l=j**q
    return part,N,M

#Iterates the sampler
def worker_test(name,q,L,n,m,max_attempt,z1,z2,stop_flag):
    nb_attempts=0
    N=0
    M=0
    representable_test_worker = [0]*L
    while (N!=n or M !=m) and (nb_attempts<max_attempt) and not stop_flag.value:
        part,N,M=worker_sampler(q,L,n,m,z1,z2)
        nb_attempts=nb_attempts+1
        if M==m:
            representable_test_worker[N-1]=1
        if N==n and M==m:
            stop_flag.value=True
    return representable_test_worker

#Helper function to unpack arguments and call worker_test
def worker_helper(args):    
    return worker_test(*args)

#Compute the maximal number of attempts per worker
def max_attempt_comp(q,n,m,delta, nworkers):
    a=m/q
    return floor(-n*((exp(1)/a)**a)*(gamma(a)*log(delta))*factorial(m)/((m**m)*exp(-m)*nworkers))

#Calibrate z1 and z2
def calibration(q,n,m):
    kappa=(m**(q+1))/n
    z1=np.exp(-m/(q*n))
    z2=(kappa**(1/q))/((q**(1/q))*gamma(1+1/q))
    return z1,z2

#Combine list of representability results obtained by the workers
def combine_workers(representable_test_workers): 
    combined_list = [int(any(elements)) for elements in zip(*representable_test_workers)]
    return combined_list

#Combine two lists of representability results
def combine_lists(list1, list2):
    combined_list = [max(x, y) for x, y in zip(list1, list2)]
    return combined_list

#Print the list of reprentable numbers that have been obtained
def print_representable(representable_test):
    print("The following numbers are representable:")
    indices = []
    for index, value in enumerate(representable_test):
        if value == 1:
            indices.append(str(index + 1))
    print(", ".join(indices))

#Test if n is representable
def single_n_test(q,L,n,m,delta):
    # Compute the number of workers
    nworkers = 1
    # Compute the maximal number of attempts per worker
    max_attempt = max_attempt_comp(q,n,m,delta,nworkers)
    # Calibrate the parameters
    z1,z2=calibration(q,n,m)
    # Create a manager to manage shared variables
    manager = mp.Manager()
    # Create a shared stop flag variable
    stop_flag = manager.Value('i', False)
    # Create a pool of worker processes
    pool = mp.Pool()
    # Use imap_unordered with the helper function
    representable_test_workers=pool.imap_unordered(worker_helper, [(name,q,L,n,m,max_attempt,z1,z2,stop_flag) for name in range(nworkers)])
    # Close the pool to prevent any new tasks
    pool.close()
    # Wait for all worker processes to complete
    pool.join()
    # Combine the results of the workers
    representable_test = combine_workers(representable_test_workers)
    return representable_test

#Test representability from L down to 1
def multiple_test(q,L,l,m,delta):
    representable_test = [0]*L
    for n in range(L, l-1, -1):
        if not representable_test[n-1]:
            print("Test the number", n)
            representable_test=combine_lists(representable_test,single_n_test(q,L,n,m,delta))
    return representable_test

if __name__ == '__main__':
    # Inputs of the programs
    while True:
        L = int(input("Enter a weight upper limit L: "))
        l = int(input("Enter a weight lower limit l: "))
        m = int(input("Enter a target length m: "))
        q = int(input("Enter a power q: "))
        delta = float(input("Enter significance level delta: "))

        if m > 0 and q > 0 and 0 < delta < 1 and L>0 and l>0:
            print("Input values are valid.")
            break
        else:
            print("Invalid input. Please make sure n, m, q and L are positive integers, and delta is a float between 0 and 1.")

    # Starts the timer
    start_time = time.time()
    representable_test=multiple_test(q,L,l,m,delta)

    #print the representable numbers obtained
    print_representable(representable_test)
    # End the timer
    end_time = time.time()
    # Calculate the elapsed time
    execution_time = end_time - start_time
    # Print the execution time
    print("Execution time: ", execution_time, "seconds")
