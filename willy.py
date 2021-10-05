from modules.globals import *
from modules.recognition import get_query
from modules.text_procesing import *
import concurrent.futures

class Willy:
    def __init__(self):
        self.no_in_question = False
        self.brute_question = None
        self.brute_answers = None
        self.token_question = None
        self.token_answers = None
        self.answer_key_words = None
    
    def run(self, q_lines):

        # READ AND PROCESS QUESTION & ANSWERS
        self.brute_question , self.brute_answers = get_query(q_lines)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            nq = executor.submit(search_no_question, self.brute_question)
            tq = executor.submit(token_string, self.brute_question)
            ta = [executor.submit(token_string, a) for a in self.token_answers]

            self.no_in_question = nq.result()
            self.token_question = tq.result()
            self.token_answers = [exe.result() for exe in ta]
            self.answer_key_words = [(word for word in answ) for answ in self.token_answers]
           

        return
    
    