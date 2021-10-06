from modules.globals import *
from modules.recognition import get_query
from modules.text_procesing import *
from googleapiclient.discovery import build 
from bs4.element import ResultSet
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

        self.search_titles = []
        self.search_snippets = []
        self.urls = []
        self.exlude_urls = []
        self.doc_name = ""

    def reset(self):
        self.search_titles = []
        self.search_snippets = []
        self.urls = []
        self.exlude_urls = []

    def google_search(self):

        results = build("customsearch","v1",developerKey=self.api_key).cse().list(q=self.brute_question,cx=self.cse_id,num=5).execute()
        if not results.get('items'): return 0 

        for r in results:
            self.search_titles.append(r['title'])
            self.search_titles.append(r['snippet'])
            url_low = r['link'].lower()
            if url_low.find("youtube") == -1 and url_low.find("anexo") == -1 and url_low.find("archivo") == -1 and url_low.find("image") == -1:
                self.urls.append(r['link'])
                if len(self.urls) == 1: self.doc_name = r['title']
            else: self.exlude_urls.append(r['link'])

        if len(self.urls) == 0: return -1
        return 1
    
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
        
        # GOOGLE SEARCH
        var = self.google_search()
        if var == 0: # Nothing to do :(
            print("No Google Results D:")
            return 
        
        # Check answer in search, snippet, doc name and star final answer
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            answ_search = executor.submit()
            answ_snippet = executor.submit()
            answ_doc_name = executor.submit()
            answ_tf_idf = executor.submit()
 

        return
    
    