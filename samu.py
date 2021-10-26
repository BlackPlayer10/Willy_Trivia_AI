from requests.api import options
from modules.globals import *
from time import sleep

class Samu:
    def __init__(self):
        self.CORRECT_ANSWER = None
        self.options_tried = []
        self.discart_options = ["A", "B", "C"]
        self.try_probably_answers = True
        self.try_probably_final_answers = True
    
    def reset(self):
        self.CORRECT_ANSWER = None
        self.options_tried = []
        self.discart_options = ["A", "B", "C"]
        self.try_probably_answers = True
        self.try_probably_final_answers = True


    def try_answer(self):
        # TRY IN ONE PHONE        
        # CHECK IF IS CORRECT - INCORRECT
        self.options_tried.append(self.discart_options[0])
        del self.discart_options[0]

    # SOLO PARA PRUEBA
    def print_probably_answer(self):
        print("PRE ANSWERS: ")
        for i in range(len(probably_answers)):
            print("-->", probably_answers[i], "<--\t",end="")
        print("\n")
        self.try_probably_answers = False
        
        
    # SOLO PARA PRUEBA
    def print_probably_final_answer(self):
        print("FINAL ANSWERS: ", end="")
        for i in range(len(probably_answers)):
            print("-->", probably_final_answers[i], "<--\t",end="")
        print("\n")
        self.try_probably_final_answers = False


    def discart_everything(self):
        return

    def check_probably_answers(self):
        global probably_answers
        if len(probably_answers) == 0: return False
        # FIX DISCART OPTIONS BUG
        #self.discart_option = probably_answers
        return True

    def check_probably_final_answers(self):
        global probably_final_answers
        if len(probably_final_answers) == 0: return False
        # FIX DISCART OPTIONS BUG
        #self.discart_option = probably_answers
        return True

    def run_check(self):
        while True:
            sleep(0.3)
            if self.check_probably_answers() and self.try_probably_answers: self.print_probably_answer()
            if self.check_probably_final_answers() and self.try_probably_final_answers: self.print_probably_final_answer()
            


