import pynlpir
import re
import sys
import csv
import io
pynlpir.open()
from hanziconv import HanziConv
from cwn import synset
import random

#split input corpus by Chinese punctuation characters and return list of sentences
def sentences(input):
    sentences_list = []
    sentence = list(re.split('(。|！|？)',input))
    for i in range(0,len(sentence)-1,2):
        sentences_list.append(sentence[i]+sentence[i+1])
    return sentences_list

#strip hanzi from non-letter characters and eliminate duplicates
def strip_list(list):
    num_removed = set([re.sub(r'\d+', '',x) for x in list])
    simpl = [HanziConv.toSimplified(x) for x in num_removed]
    return simpl

#retrieves lexical information about a list of words
def retrieve_lex_info(wordlist):
    lex_info = {}
    for word in wordlist:
        l = [None,None,None,None]
        lex_info[word] = None
        s = synset(HanziConv.toTraditional(word))
        if s.synonyms:
            l[0] = strip_list(s.synonyms)
            lex_info[word] = l
        if s.antonyms:
            l[1] = strip_list(s.antonyms)
            lex_info[word] = l
        if s.hyponyms:
            l[2] = strip_list(s.hyponyms)
            lex_info[word] = l
        if s.hypernyms:
            l[3] = strip_list(s.hypernyms)
            lex_info[word] = l
    return lex_info

def retrieve_synonyms(lex_info_object):
    synonyms = {}
    for word, lex_info in lex_info_object.items():
        if lex_info:
            if lex_info[0]:
                synonyms[word] = lex_info[0]
    return synonyms

def retrieve_antonyms(lex_info_object):
    antonyms = {}
    for word, lex_info in lex_info_object.items():
        if lex_info:
            if lex_info[1]:
                antonyms[word] = lex_info[1]
    return antonyms

def retrieve_hyponyms(lex_info_object):
    hyponyms = {}
    for word, lex_info in lex_info_object.items():
        if lex_info:
            if lex_info[2]:
                hyponyms[word] = lex_info[2]
    return hyponyms

def retrieve_hypernyms(lex_info_object):
    hypernyms = {}
    for word, lex_info in lex_info_object.items():
        if lex_info:
            if lex_info[3]:
                hypernyms[word] = lex_info[3]
    return hypernyms

#reads a file with just one(!) line
def import_data(fileName):
    with io.open(fileName,'r',encoding='utf8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            return row
    f.close()

#writes toefl multiple choice like test to new file for evaluating purposes
def write_results(fileName,corpus):
    with io.open("result_"+fileName,'w',encoding='utf8') as f:
        count = 1
        for text in corpus:
            conv = HanziConv.toSimplified(text)
            segm = pynlpir.segment(conv, pos_tagging=False)
            key_words = pynlpir.get_key_words(conv, weighted=False)

            lex_info_obj = retrieve_lex_info(key_words)
            synonyms = retrieve_synonyms(lex_info_obj)
            antonyms = retrieve_antonyms(lex_info_obj)
            hyponyms = retrieve_hyponyms(lex_info_obj)
            hypernyms = retrieve_hypernyms(lex_info_obj)

            f.write("Text: "+str(count)+"\n")
            f.write(conv+"\n")

            f.write("\nSynonyms: ")
            f.write(str(synonyms))
            f.write("\nAntonyms: ")
            f.write(str(antonyms))
            f.write("\nHyponyms: ")
            f.write(str(hyponyms))
            f.write("\nHypernyms: ")
            f.write(str(hypernyms))

            f.write("\n\nQuestions: \n")
            
            for sentence in sentences(conv):
                for word, antonym in antonyms.items():
                    if bool(re.search(word, sentence)):
                        f.write("\n"+re.sub(word,'____',sentence))

                        if antonyms.get(word):
                            distractor_same_len_char = [ant for ant in antonym if len(ant)==len(word)]
                            distractor_diff_len_char = [ant for ant in antonym if len(ant)!=len(word)]

                        if distractor_same_len_char:
                            antonym = distractor_same_len_char
                        elif distractor_diff_len_char:
                            antonym = distractor_diff_len_char
                            
                        distractor = antonym[random.randint(0,len(antonym)-1)]
                        answer = [word,distractor]
                        if random.randint(0,1) == 0:
                            f.write("\nA: " + answer[0] + "\tB: " + answer[1])
                            if(len(antonyms.get(word)) > 1): #if there is just antonym keep it
                                antonyms.get(word).remove(distractor)
                        else:
                            f.write("\nA: " + answer[1] + "\tB: " + answer[0])
                            if(len(antonyms.get(word)) > 1):
                                antonyms.get(word).remove(distractor)
            count+=1
            f.write("\n\n\n")
    f.close()

if __name__ == '__main__':
    readFile = str(sys.argv[1])
    corpus = import_data(readFile)
    write_results(readFile,corpus)
