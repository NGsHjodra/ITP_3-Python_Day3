# import the module
from decimal import *
import multiprocessing
import time
import concurrent.futures

# res = Decimal(0)

def bbp_term(k, n):
    getcontext().prec=n+1

    return (1 / (Decimal(16) ** k) *
        (Decimal(4) / (8 * k + 1) -
        Decimal(2) / (8 * k + 4) -
        Decimal(1) / (8 * k + 5) -
        Decimal(1) / (8 * k + 6)))

# calculate pi using the BBP formula with n digits using processes
# check number of cores and use pool of processes

def pi_multiprocessing(n):
    num_cores = multiprocessing.cpu_count()
    getcontext().prec=n+1

    # create a pool of processes
    pool = multiprocessing.Pool(num_cores)
    res = Decimal(0)
    
    terms = pool.starmap(bbp_term, [(k, n) for k in range(n + 1)])

    for term in terms:
        res += term

    return res 

def pi_future(n):
    getcontext().prec=n+1
    futures = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for k in range(n + 1):
            futures.append(executor.submit(bbp_term, k, n))

    res = Decimal(0)
    
    for future in futures:
        res += future.result()

    return res

if __name__ == '__main__':
    N = 150

    start = time.time()
    print(str(pi_multiprocessing(N))[:20])
    end = time.time()

    print("Time taken: ", end - start)

    start = time.time()
    print(str(pi_future(N))[:20])
    end = time.time()

    print("Time taken: ", end - start)