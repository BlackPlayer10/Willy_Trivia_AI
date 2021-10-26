from ctypes import windll
from samu import Samu
from willy import Willy
import concurrent.futures

def main():

    print("\n\t\t *** WILLY 1.0 *** \n")
    WILLY = Willy()
    SAMU = Samu()

    while True:
        
        x = input("Input Question lines (ENTER = 3): ")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            W = executor.submit(WILLY.run, 3 if not x else int(x))
            #S = executor.submit(SAMU.run_check)
            W.result()
            #S.result()

        WILLY.reset()
        #SAMU.reset()

        print("-"*50)
        
main()