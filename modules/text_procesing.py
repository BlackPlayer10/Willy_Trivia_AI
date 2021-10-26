from nltk import corpus, word_tokenize

trash_terms = "-.!«•»;',<>()/\\[]¿?%“”*+@#$^&*_={|}\"~`\n"
trash_words = corpus.stopwords.words('spanish') + ["-"]
del trash_words[163] # estados

def replace_sign(letter):
    if letter == "á": return "a"
    if letter == "é": return "e"
    if letter == "í": return "i"
    if letter == "ó": return "o"
    if letter in "úü": return "u"
    return letter

def search_no_question(sentence): # By reference
    new_str = ""
    i, size = 0, len(sentence)
    while i < size:
        if sentence[i] in "'\"“”": 
            i+=1
            while sentence[i] not in "'\"“”": i+=1
            i+=1  
        new_str+=sentence[i]
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


