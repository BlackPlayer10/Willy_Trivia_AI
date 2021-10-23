from yaml import parse
from modules.globals import *
from modules.recognition import get_query
from modules.text_procesing import *
from googleapiclient.discovery import build 
#from bs4.element import ResultSet
from bs4 import BeautifulSoup
import requests
import concurrent.futures

class Willy:
    def __init__(self):

        # Load keys
        keys = open("modules//keys.txt", "r")
        self.api_key = keys.readline()[:-1]
        self.cse_id = keys.readline()
        keys.close()

        self.no_in_question = False
        self.brute_question = None
        self.brute_answers = None
        self.token_question = None
        self.token_answers = None
        self.answer_key_words = None
        self.data = []

        self.search_titles = []
        self.search_snippets = []
        self.doc_name = ""

        self.urls = []
        self.exlude_urls = []

        self.preliminary_scores = [] # Lista de listas de los score de googl_search, doc_name y snipper
        self.final_answ_score = [] # Scores de respuestas

        # probably_answers (GLOBAL) lista con las respuestas en orden

    def reset(self):
        global probably_answers 
        probably_answers = []

        self.search_titles = []
        self.search_snippets = []

        self.urls = []
        self.exclude_urls = []

        self.preliminary_scores = []
        self.final_answ_score = []

    def parser_aux(self, tag):
        token = token_string(tag.get_text(strip=True, separator=" "))
        for word in self.answer_key_words:
            if word in token:
                self.data.append(token)
                return

    def parse(self):
        i = 1
        for url in self.urls + self.exclude_urls:
            i+=1
            print("Parsing url Nro", i)
            self.data = []
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                found = [executor.submit(soup.find_all, tag) for tag in ["li","p"]]
                for exe in found: 
                    for tag in exe.result(): self.parser_aux(tag)
            if len(self.data) > 0: return 1
        return 0
        

    def google_search(self):

        results = build("customsearch","v1",developerKey=self.api_key).cse().list(q=self.brute_question,cx=self.cse_id,num=5).execute()
        if not results.get('items'): return 0 

        for r in results:
            self.search_titles.append(r['title'])
            self.search_snippets.append(r['snippet'])
            url_low = r['link'].lower()
            if url_low.find("youtube") == -1 and url_low.find("anexo") == -1 and url_low.find("archivo") == -1 and url_low.find("image") == -1:
                self.urls.append(r['link'])
                if len(self.urls) == 1: self.doc_name = r['title']
            else: self.exclude_urls.append(r['link'])

        if len(self.urls) == 0: return -1
        return 1
    
    def pre_score(self, code): # Se busca respuesta en titulo, en busqueda y en snippets
        
        if code == "snip": token = token_string(" ".join(self.search_snippets))
        elif code == "goog": token = token_string(" ".join(self.search_titles))
        elif code == "docn": token = token_string(self.doc_name)

        score = [0,0,0]
        for word in token:
            for i in range(len(self.token_answers)):
                if word in self.token_answers[i]: score[i] += 1
        
        self.preliminary_scores.append(score[:])
        return True

    def edit_possible_answers(self): # Se ejecuta despues de haber buscado respuesta en titulo, busqueda y snip
        global probably_answers
        general_score = [0,0,0]
        for s_list in self.preliminary_scores:
            for i in range(len(s_list)):
                general_score[i] += s_list[i]
        general_score = [[general_score[i], chr(i+65)] for i in range(3)]
        general_score.sort()
        probably_answers = [general_score[i][1] for i in range(3)]
        # NO IN QUESTION (La respuesta es lo que menos aparece)
        if self.no_in_question: probably_answers = probably_answers[::-1]  
        return

    def no_final_answer(self):

        return

    def final_answer(self):
        return

    def run(self, q_lines):

        # READ AND PROCESS QUESTION & ANSWERS
        self.brute_question , self.brute_answers = get_query(q_lines)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            nq = executor.submit(search_no_question, self.brute_question)
            tq = executor.submit(token_string, self.brute_question)
            ta = [executor.submit(token_string, a) for a in self.brute_answers]

            self.no_in_question = nq.result()
            self.token_question = tq.result()
            self.token_answers = [exe.result() for exe in ta]
            self.answer_key_words = [(word for word in answ) for answ in self.token_answers]
        
        # GOOGLE SEARCH
        var = self.google_search()
        if var == 0:
            print("No Google Results D:")
            return 
        
        # Check answer in search, snippet, doc name and start final answer
 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            scores1 = [executor.submit(self.pre_score, c) for c in ["snip", "goog", "docn"]]
            parser = executor.submit(self.parse)
            if parse.result(): f_answ = executor.submit(self.final_answer) if not self.no_in_question else executor.submit(self.no_final_answer())
            else: 
                print('NO ANSWERS ANYWHERE :(')
                return

            for i in range(3): scores1[i].result()
            self.edit_possible_answers()

            

        return
    
    