from samu import Samu
from willy import Willy
import concurrent.futures

def main():

    
    WILLY = Willy()
    SAMU = Samu()

    while True:
        print("\n\t\t *** WILLY 1.0 *** \n")
        x = input("Input Question lines (ENTER = 3): ")
        WILLY.run(3 if not x else int(x))
        WILLY.reset()
        print("-"*50)
        
main()