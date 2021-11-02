from nltk import corpus, word_tokenize

trash_terms = "-.,:;!«•»[]¿?↑'<>()“”‘’/\\%*+@#$^&*_={|}\"~`ªº\n"
trash_words = corpus.stopwords.words('spanish') + ["-"]
del trash_words[163] # estados

def replace_sign(letter):
    if letter in "áà": return "a"
    if letter in "éè": return "e"
    if letter in "íì": return "i"
    if letter in "óò": return "o"
    if letter in "úùü": return "u"
    return letter

def search_no_question(sentence): # By reference
    new_str = ""
    i, size = 0, len(sentence)
    while i < size:
        if sentence[i] in "'\"“”": 
            i+=1
            while i < size and sentence[i] not in "'\"“”": i+=1
            i+=1  
        if i < size: new_str+=sentence[i] # Es posible que se cierre comilla y se abra justo otra?
        i+=1
    if "no" in word_tokenize(new_str): return True
    return False

def token_string(sentence): # By reference
    new_str = ""
    for letter in sentence.lower():
        if letter not in trash_terms: new_str += replace_sign(letter)
        if letter == "-": new_str += " " # Arregla bug palabras compuestas ejemp: '1937-septiembre'
    new_str = word_tokenize(new_str)
    last_str = [word for word in new_str if word not in trash_words]
    return last_str

def procces_google_query(sentence):
    query = ""
    for letter in sentence:
        if letter not in trash_terms: query += letter
    return query